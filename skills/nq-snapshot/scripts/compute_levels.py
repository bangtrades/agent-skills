#!/usr/bin/env python3
"""
compute_levels.py — Helper for nq-snapshot skill.

Reads chart state from stdin as JSON, emits computed levels (distances, channel
position, R-multiples, vector tags) as JSON to stdout. Keeps Claude's inline
arithmetic clean and avoids drift.

Input schema (stdin, JSON):
{
  "timeframe": "5m" | "15m" | "60m",
  "last": 29158.00,
  "study_values": {
    "BT VWAP": {"VWAP": 29279.85},
    "BT MA Bands": {
      "Anchor MA": 29158.21,
      "MA 2": 29151.32,
      "MA 3": 29174.07,
      "MA 5": 29185.85,
      "MA 6": 29172.09,
      "MA 7": 29204.18,
      "Upper Band": 29184.84,
      "Lower Band": 29131.57
    },
    "BT Volatility Envelope ": {
      "Envelope Base": 29270.33,
      "Envelope Top Min": 29403.72,
      "Envelope Top Max": 29503.76,
      "Envelope Bottom Min": 29136.93,
      "Envelope Bottom Max": 29036.89
    },
    "BT Volatility Envelope + Delta": {
      "Envelope Base": 29171.81,
      "Envelope Top Min": 29216.02,
      "Envelope Bottom Min": 29127.61,
      "delta": 2707.59,
      "delta_pct": 95.95,
      "buy_vol": 2764.80,
      "sell_vol": 57.20,
      "flip_signal": 1.0
    }
  },
  "ohlcv_window": {
    "open": 29456.75,
    "high": 29471.50,
    "low": 29121.25,
    "close": 29158.00,
    "range": 350.25,
    "bar_count": 200,
    "avg_volume": 3592
  },
  "discipline": {
    "r1_cap_dollars_per_pt": 4,
    "r3_daily_cap": 200
  }
}

Output schema (stdout, JSON):
{
  "timeframe": "5m",
  "last": 29158.00,
  "distances": {
    "vwap": -121.85,
    "k_upper": 26.84,
    "k_lower": -26.43,
    "k_anchor": 0.21,
    "envelope_tight_top": 58.02,
    "envelope_tight_bottom": -30.39,
    "envelope_wide_top_min": 245.72,
    "envelope_wide_bottom_min": -21.07
  },
  "channel_position_pct": 49.6,
  "ma_stack": {
    "ordering": ["MA 2", "Anchor MA", "MA 6", "MA 3", "MA 5", "MA 7"],
    "stack_direction": "ascending" | "descending" | "braided",
    "spread_pts": 52.86
  },
  "order_flow": {
    "delta_pct": 95.95,
    "buy_sell_ratio": 48.34,
    "dominance": "extreme_buy",
    "absorption_flag": true,
    "flip_active": true
  },
  "vector_tags": {
    "vwap_behavior": "below_vwap_strong",
    "ma_stack": "braided",
    "aggression": "extreme_buy_absorption"
  },
  "r1_risk_math": {
    "size_micros_at_r1_cap": 2,
    "max_risk_at_8pt_stop": 16,
    "stops_available_in_r3_budget": 12
  },
  "warnings": []
}

Usage:
    echo '{"timeframe":"5m",...}' | python3 compute_levels.py
"""

import sys
import json


def safe_get(d, path, default=None):
    """Safely traverse a nested dict."""
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def compute(input_data):
    last = float(input_data.get("last", 0))
    timeframe = input_data.get("timeframe", "unknown")
    sv = input_data.get("study_values", {})
    discipline = input_data.get("discipline", {})
    warnings = []

    # === Distances ===
    distances = {}

    vwap = safe_get(sv, ["BT VWAP", "VWAP"])
    if vwap is not None:
        distances["vwap"] = round(last - vwap, 2)

    ma = sv.get("BT MA Bands", {})
    if ma:
        for key, dest in [
            ("Upper Band", "k_upper"),
            ("Lower Band", "k_lower"),
            ("Anchor MA", "k_anchor"),
        ]:
            if key in ma:
                distances[dest] = round(last - ma[key], 2)

    env_tight = sv.get("BT Volatility Envelope ", {}) or sv.get(
        "BT Volatility Envelope", {}
    )
    if env_tight:
        for key, dest in [
            ("Envelope Top Min", "envelope_tight_top"),
            ("Envelope Bottom Min", "envelope_tight_bottom"),
            ("Envelope Top Max", "envelope_wide_top_min"),
            ("Envelope Bottom Max", "envelope_wide_bottom_min"),
        ]:
            if key in env_tight:
                distances[dest] = round(last - env_tight[key], 2)

    env_delta = sv.get("BT Volatility Envelope + Delta", {}) or sv.get(
        "BT Volatility Envelope + Delta ", {}
    )

    # === Channel position ===
    channel_position_pct = None
    if ma and "Upper Band" in ma and "Lower Band" in ma:
        upper = ma["Upper Band"]
        lower = ma["Lower Band"]
        width = upper - lower
        if width > 0:
            pos = (last - lower) / width
            channel_position_pct = round(pos * 100, 1)
        else:
            warnings.append("MA Bands width is zero or negative — possible data artifact")

    # === MA stack ===
    ma_stack = {}
    if ma:
        ma_keys = ["MA 2", "Anchor MA", "MA 3", "MA 5", "MA 6", "MA 7"]
        avail = [(k, ma[k]) for k in ma_keys if k in ma]
        ordered = sorted(avail, key=lambda x: x[1])
        ma_stack["ordering"] = [k for k, _ in ordered]
        if avail:
            spread = max(v for _, v in avail) - min(v for _, v in avail)
            ma_stack["spread_pts"] = round(spread, 2)
        # Detect stack direction by comparing the expected short→long order
        # Short MAs (MA 2, Anchor) vs Long MAs (MA 5, MA 7)
        if "MA 2" in ma and "MA 7" in ma:
            short_avg = ma["MA 2"]
            long_avg = ma["MA 7"]
            diff = short_avg - long_avg
            atr_proxy = ma_stack.get("spread_pts", 50)
            if abs(diff) < 0.2 * atr_proxy:
                ma_stack["stack_direction"] = "braided"
            elif diff > 0:
                ma_stack["stack_direction"] = "ascending"  # bullish stack
            else:
                ma_stack["stack_direction"] = "descending"  # bearish stack

    # === Order flow ===
    order_flow = {}
    vector_tags = {}
    if env_delta:
        delta_pct = env_delta.get("delta_pct")
        buy_vol = env_delta.get("buy_vol", 0)
        sell_vol = env_delta.get("sell_vol", 0)
        flip = env_delta.get("flip_signal", 0)

        if delta_pct is not None:
            order_flow["delta_pct"] = delta_pct
            if buy_vol > 0 and sell_vol > 0:
                ratio = buy_vol / sell_vol if buy_vol >= sell_vol else -(sell_vol / buy_vol)
                order_flow["buy_sell_ratio"] = round(abs(ratio), 2)
            else:
                order_flow["buy_sell_ratio"] = None

            abs_pct = abs(delta_pct)
            if abs_pct > 90:
                dominance = "extreme_buy" if delta_pct > 0 else "extreme_sell"
            elif abs_pct > 70:
                dominance = "strong_buy" if delta_pct > 0 else "strong_sell"
            elif abs_pct > 30:
                dominance = "moderate_buy" if delta_pct > 0 else "moderate_sell"
            else:
                dominance = "neutral"
            order_flow["dominance"] = dominance
            order_flow["absorption_flag"] = abs_pct > 85
            order_flow["flip_active"] = bool(flip and flip >= 1.0)

            if abs_pct > 85:
                vector_tags["aggression"] = (
                    "extreme_buy_absorption"
                    if delta_pct > 0
                    else "extreme_sell_absorption"
                )
            elif abs_pct > 50:
                vector_tags["aggression"] = (
                    "buy_dominant" if delta_pct > 0 else "sell_dominant"
                )
            else:
                vector_tags["aggression"] = "neutral_flow"

    # === Vector tags from VWAP / channel ===
    if "vwap" in distances:
        vd = distances["vwap"]
        # Use channel width as ATR proxy
        atr_proxy = 50.0
        if ma_stack.get("spread_pts"):
            atr_proxy = max(ma_stack["spread_pts"], 30)
        if abs(vd) < 0.3 * atr_proxy:
            vector_tags["vwap_behavior"] = "at_vwap"
        elif vd < -0.5 * atr_proxy:
            vector_tags["vwap_behavior"] = "below_vwap_strong"
        elif vd < 0:
            vector_tags["vwap_behavior"] = "below_vwap_moderate"
        elif vd > 0.5 * atr_proxy:
            vector_tags["vwap_behavior"] = "above_vwap_strong"
        else:
            vector_tags["vwap_behavior"] = "above_vwap_moderate"

    if ma_stack.get("stack_direction"):
        vector_tags["ma_stack"] = ma_stack["stack_direction"]

    if channel_position_pct is not None:
        if channel_position_pct < 0:
            vector_tags["k_channel_position"] = "below_channel"
        elif channel_position_pct < 25:
            vector_tags["k_channel_position"] = "lower_quartile"
        elif channel_position_pct < 50:
            vector_tags["k_channel_position"] = "lower_half"
        elif channel_position_pct < 75:
            vector_tags["k_channel_position"] = "upper_half"
        elif channel_position_pct <= 100:
            vector_tags["k_channel_position"] = "upper_quartile"
        else:
            vector_tags["k_channel_position"] = "above_channel"

    # === R1 risk math ===
    r1_risk_math = {}
    r1_cap = discipline.get("r1_cap_dollars_per_pt", 4)
    r3_cap = discipline.get("r3_daily_cap", 200)
    size_micros = r1_cap // 2  # MNQ micros = $2/pt each
    r1_risk_math["size_micros_at_r1_cap"] = int(size_micros)
    r1_risk_math["dollars_per_point"] = r1_cap
    # Default 8-pt stop
    risk_per_trade = r1_cap * 8
    r1_risk_math["max_risk_at_8pt_stop"] = risk_per_trade
    if risk_per_trade > 0:
        r1_risk_math["stops_available_in_r3_budget"] = int(r3_cap / risk_per_trade)

    # === Cursor-position artifact warning ===
    # If K Upper or K Lower is more than 3× spread away from current price, suspect artifact
    if ma_stack.get("spread_pts") and ma.get("Upper Band") and ma.get("Lower Band"):
        spread = ma_stack["spread_pts"]
        if abs(last - ma["Upper Band"]) > 3 * spread or abs(last - ma["Lower Band"]) > 3 * spread:
            warnings.append(
                "BT MA Bands values may be cursor-position artifacts — Upper/Lower seem far from current price. "
                "Visually verify from screenshot before relying on them."
            )

    return {
        "timeframe": timeframe,
        "last": last,
        "distances": distances,
        "channel_position_pct": channel_position_pct,
        "ma_stack": ma_stack,
        "order_flow": order_flow,
        "vector_tags": vector_tags,
        "r1_risk_math": r1_risk_math,
        "warnings": warnings,
    }


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}), file=sys.stderr)
        sys.exit(1)

    result = compute(input_data)
    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
