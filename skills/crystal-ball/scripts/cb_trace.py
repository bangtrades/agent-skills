#!/usr/bin/env python3
"""cb_trace.py — Crystal Ball ladder computation + price trace.

Computes the T1-T5 ladder from a CB drawing's two anchors, then traces an OHLCV
series through it: first-touch of every level, bars-from-anchor, dwell gaps, and
the T5 overshoot. Works for bullish and bearish CBs. Deterministic — use this
instead of hand-computing so the numbers stay identical across samples.

Usage:
  python3 cb_trace.py --ohlcv bars.csv --anchor-price 28885 \\
      --unit-price 29241.47 --direction bull --anchor-unix 1779253200

  --ohlcv         CSV with header: time_unix,open,high,low,close,volume
                  (a time_pt column, if present, is ignored)
  --anchor-price  the CB '0' level  (expansion low for bull, high for bear)
  --unit-price    the CB '1.0' / T1 level (the drawing's 2nd anchor price)
  --direction     bull | bear
  --anchor-unix   unix time of the anchor bar (trace starts here; optional —
                  defaults to the first bar in the CSV)
  --tz-offset     hours from UTC for display times (default -7, US/Pacific PDT)

Output: a level table + trace to stdout.
"""
import argparse, csv, datetime, sys

COEFFS = [("0", 0.0), ("0.618 CISD", 0.618), ("0.877", 0.877),
          ("T1", 1.0), ("T2", 1.236), ("T3", 1.618), ("T4", 1.902), ("T5", 2.38)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ohlcv", required=True)
    ap.add_argument("--anchor-price", type=float, required=True)
    ap.add_argument("--unit-price", type=float, required=True)
    ap.add_argument("--direction", choices=["bull", "bear"], required=True)
    ap.add_argument("--anchor-unix", type=int, default=None)
    ap.add_argument("--tz-offset", type=float, default=-7.0)
    a = ap.parse_args()

    tz = datetime.timezone(datetime.timedelta(hours=a.tz_offset))
    def fmt(u): return datetime.datetime.fromtimestamp(u, tz).strftime("%Y-%m-%d %H:%M")

    bars = []
    with open(a.ohlcv) as f:
        for r in csv.DictReader(f):
            try:
                bars.append({"u": int(float(r["time_unix"])), "o": float(r["open"]),
                             "h": float(r["high"]), "l": float(r["low"]),
                             "c": float(r["close"]), "v": float(r.get("volume", 0) or 0)})
            except (KeyError, ValueError):
                continue
    if not bars:
        sys.exit("no bars parsed — expected header time_unix,open,high,low,close,volume")
    bars.sort(key=lambda b: b["u"])

    p0 = a.anchor_price
    unit = a.unit_price - p0          # signed; negative for a bear CB
    if a.direction == "bull" and unit <= 0:
        sys.exit("bull CB but unit-price <= anchor-price — check inputs/direction")
    if a.direction == "bear" and unit >= 0:
        sys.exit("bear CB but unit-price >= anchor-price — check inputs/direction")
    level = lambda c: p0 + c * unit

    # locate the anchor bar
    if a.anchor_unix is not None:
        ai = next((i for i, b in enumerate(bars) if b["u"] >= a.anchor_unix), 0)
    else:
        ai = 0

    print("=" * 64)
    print(f"  CRYSTAL BALL TRACE  —  {a.direction.upper()}  CB")
    print("=" * 64)
    print(f"  anchor 0      {p0:>11.2f}   {fmt(bars[ai]['u'])}  (bar #{ai})")
    print(f"  unit (0->T1)  {abs(unit):>11.2f}")
    print(f"  bars in file  {len(bars)}   trace from bar #{ai}")
    print("-" * 64)
    print(f"  {'level':<13}{'price':>11}{'first-touch':>20}{'bars':>6}{'gap':>5}")
    print("-" * 64)

    touch = lambda b, px: (b["h"] >= px) if a.direction == "bull" else (b["l"] <= px)
    prev_bi = None
    t5_bi = None
    for name, c in COEFFS:
        px = level(c)
        bi = next((i for i in range(ai, len(bars)) if touch(bars[i], px)), None)
        if bi is None:
            print(f"  {name:<13}{px:>11.2f}{'(not reached)':>20}{'':>6}{'':>5}")
            continue
        gap = "" if prev_bi is None else str(bi - prev_bi)
        print(f"  {name:<13}{px:>11.2f}{fmt(bars[bi]['u']):>20}{bi - ai:>6}{gap:>5}")
        prev_bi = bi
        if name == "T5":
            t5_bi = bi

    print("-" * 64)
    # T5 overshoot + current position
    t5 = level(2.38)
    if t5_bi is not None:
        if a.direction == "bull":
            ext = max(b["h"] for b in bars[t5_bi:])
            print(f"  T5 {t5:.2f} reached {fmt(bars[t5_bi]['u'])}  |  high since T5 {ext:.2f}  (+{ext - t5:.1f} past T5)")
        else:
            ext = min(b["l"] for b in bars[t5_bi:])
            print(f"  T5 {t5:.2f} reached {fmt(bars[t5_bi]['u'])}  |  low since T5 {ext:.2f}  ({t5 - ext:.1f} past T5)")
    last = bars[-1]
    pos = (last["c"] - p0) / unit if unit else 0.0
    print(f"  last bar {fmt(last['u'])}  close {last['c']:.2f}  =  {pos:.3f}x unit "
          f"(ladder coeff)")
    print("=" * 64)


if __name__ == "__main__":
    main()
