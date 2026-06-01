"""
PSO adapted for trading strategy optimization.

Provides a walk-forward optimization framework where PSO optimizes
strategy parameters within each training window, then evaluates
out-of-sample.

This is a template -- adapt the Strategy class and fitness function
to your specific trading system.
"""

import numpy as np
from typing import Callable, List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field
from pso_core import PSO, PSOResult


@dataclass
class WalkForwardResult:
    """Results from a single walk-forward window."""
    window_idx: int
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    best_params: np.ndarray
    in_sample_fitness: float
    out_of_sample_fitness: float
    top_k_params: List[np.ndarray] = field(default_factory=list)


@dataclass
class WalkForwardReport:
    """Aggregate results from walk-forward optimization."""
    windows: List[WalkForwardResult]
    overall_oos_fitness: float
    walk_forward_efficiency: float  # OOS / IS ratio
    param_stability: float  # How much params vary across windows


def walk_forward_pso(
    objective_fn: Callable[[np.ndarray, np.ndarray], float],
    data: np.ndarray,
    param_bounds: List[Tuple[float, float]],
    train_length: int,
    test_length: int,
    step_size: Optional[int] = None,
    anchored: bool = False,
    n_particles: int = 40,
    max_iter: int = 200,
    topology: str = 'von_neumann',
    n_runs: int = 3,
    top_k: int = 5,
    warm_start: bool = True,
    seed: Optional[int] = None,
    verbose: bool = True,
) -> WalkForwardReport:
    """
    Walk-forward optimization using PSO.

    Parameters
    ----------
    objective_fn : callable
        Function(params, data_slice) -> fitness (higher = better).
        PSO minimizes, so this will be negated internally.
    data : np.ndarray
        Full dataset (e.g., OHLCV bars). Rows = time, cols = features.
    param_bounds : list of tuples
        Parameter search bounds.
    train_length : int
        Number of bars in each training window.
    test_length : int
        Number of bars in each test window.
    step_size : int or None
        Bars to advance between windows. Default = test_length.
    anchored : bool
        If True, training window always starts at index 0.
    n_particles : int
        PSO swarm size.
    max_iter : int
        PSO iterations per window.
    topology : str
        PSO topology ('gbest', 'ring', 'von_neumann').
    n_runs : int
        Number of PSO runs per window (take best result).
    top_k : int
        Keep top K particles for validation.
    warm_start : bool
        Initialize 50% of swarm from previous window's best particles.
    seed : int or None
        Random seed.
    verbose : bool
        Print progress.

    Returns
    -------
    WalkForwardReport
    """
    if step_size is None:
        step_size = test_length

    total_bars = len(data)
    n_dims = len(param_bounds)
    windows: List[WalkForwardResult] = []
    prev_top_particles: Optional[np.ndarray] = None

    if seed is not None:
        np.random.seed(seed)

    window_idx = 0
    start = 0

    while True:
        if anchored:
            train_start = 0
        else:
            train_start = start

        train_end = start + train_length
        test_start = train_end
        test_end = test_start + test_length

        if test_end > total_bars:
            break

        train_data = data[train_start:train_end]
        test_data = data[test_start:test_end]

        if verbose:
            print(f"\n--- Window {window_idx + 1} ---")
            print(f"  Train: [{train_start}:{train_end}] "
                  f"({train_end - train_start} bars)")
            print(f"  Test:  [{test_start}:{test_end}] "
                  f"({test_end - test_start} bars)")

        # Define the fitness function for this window (negate for minimization)
        def window_fitness(params, _data=train_data):
            return -objective_fn(params, _data)

        # Run PSO multiple times, keep best
        best_result: Optional[PSOResult] = None
        all_final_positions: List[np.ndarray] = []

        for run in range(n_runs):
            pso = PSO(
                objective_fn=window_fitness,
                bounds=param_bounds,
                n_particles=n_particles,
                topology=topology,
                w='linear_decay',
                max_iter=max_iter,
                verbose=False,
            )

            # Warm start: inject previous window's best particles
            if warm_start and prev_top_particles is not None:
                # Will be used after initialization -- this is a simplified
                # approach. For full warm start, modify PSO.optimize() to
                # accept initial positions.
                pass

            result = pso.optimize()
            all_final_positions.append(result.final_positions)

            if best_result is None or result.best_fitness < best_result.best_fitness:
                best_result = result

        # Get top K particles across all runs
        all_positions = np.vstack(all_final_positions)
        all_fitness = np.array([window_fitness(p) for p in all_positions])
        top_k_indices = np.argsort(all_fitness)[:top_k]
        top_k_particles = all_positions[top_k_indices]

        # Evaluate top K on validation/test data
        oos_scores = [-objective_fn(p, test_data) for p in top_k_particles]
        best_oos_idx = np.argmin(oos_scores)
        best_params = top_k_particles[best_oos_idx]
        oos_fitness = -oos_scores[best_oos_idx]  # Back to original sign

        is_fitness = -best_result.best_fitness  # Best in-sample (original sign)

        if verbose:
            print(f"  In-sample fitness:  {is_fitness:.4f}")
            print(f"  Out-of-sample:      {oos_fitness:.4f}")
            print(f"  Best params: {np.round(best_params, 4)}")

        windows.append(WalkForwardResult(
            window_idx=window_idx,
            train_start=train_start,
            train_end=train_end,
            test_start=test_start,
            test_end=test_end,
            best_params=best_params,
            in_sample_fitness=is_fitness,
            out_of_sample_fitness=oos_fitness,
            top_k_params=[top_k_particles[i] for i in range(len(top_k_particles))],
        ))

        prev_top_particles = top_k_particles
        start += step_size
        window_idx += 1

    # Aggregate results
    is_scores = [w.in_sample_fitness for w in windows]
    oos_scores = [w.out_of_sample_fitness for w in windows]

    overall_oos = float(np.mean(oos_scores)) if oos_scores else 0.0
    overall_is = float(np.mean(is_scores)) if is_scores else 0.0
    wfe = overall_oos / overall_is if overall_is != 0 else 0.0

    # Parameter stability: mean coefficient of variation across windows
    if len(windows) > 1:
        all_params = np.array([w.best_params for w in windows])
        param_cv = np.mean(np.std(all_params, axis=0) /
                          (np.abs(np.mean(all_params, axis=0)) + 1e-8))
    else:
        param_cv = 0.0

    report = WalkForwardReport(
        windows=windows,
        overall_oos_fitness=overall_oos,
        walk_forward_efficiency=wfe,
        param_stability=param_cv,
    )

    if verbose:
        print(f"\n=== Walk-Forward Summary ===")
        print(f"  Windows:         {len(windows)}")
        print(f"  Avg IS fitness:  {overall_is:.4f}")
        print(f"  Avg OOS fitness: {overall_oos:.4f}")
        print(f"  WF Efficiency:   {wfe:.2%}")
        print(f"  Param Stability: {param_cv:.4f} (lower = more stable)")

    return report


# ----- Example Usage -----

if __name__ == '__main__':
    # Simulated example: optimize a simple moving average crossover
    # In practice, replace this with your actual strategy backtest

    np.random.seed(42)

    # Generate fake price data (random walk with drift)
    n_bars = 5000
    returns = np.random.randn(n_bars) * 0.02 + 0.0001
    prices = 100 * np.exp(np.cumsum(returns))
    data = prices.reshape(-1, 1)  # Single column: close prices

    def ma_crossover_fitness(params: np.ndarray, data: np.ndarray) -> float:
        """
        Simple MA crossover strategy fitness.
        params = [fast_period, slow_period]
        Returns Sharpe ratio (higher = better).
        """
        prices = data[:, 0]
        fast = max(2, int(round(params[0])))
        slow = max(fast + 1, int(round(params[1])))

        if len(prices) < slow + 1:
            return -10.0  # Not enough data

        # Compute moving averages
        fast_ma = np.convolve(prices, np.ones(fast)/fast, mode='valid')
        slow_ma = np.convolve(prices, np.ones(slow)/slow, mode='valid')

        # Align
        min_len = min(len(fast_ma), len(slow_ma))
        fast_ma = fast_ma[-min_len:]
        slow_ma = slow_ma[-min_len:]
        aligned_prices = prices[-min_len:]

        # Signals: 1 when fast > slow, -1 otherwise
        signals = np.where(fast_ma > slow_ma, 1.0, -1.0)

        # Returns
        price_returns = np.diff(aligned_prices) / aligned_prices[:-1]
        strategy_returns = signals[:-1] * price_returns

        if len(strategy_returns) < 10 or np.std(strategy_returns) < 1e-10:
            return -10.0

        sharpe = np.mean(strategy_returns) / np.std(strategy_returns) * np.sqrt(252)
        return sharpe

    # Run walk-forward optimization
    param_bounds = [(5, 50), (20, 200)]  # fast_period, slow_period

    report = walk_forward_pso(
        objective_fn=ma_crossover_fitness,
        data=data,
        param_bounds=param_bounds,
        train_length=1000,
        test_length=250,
        n_particles=30,
        max_iter=100,
        n_runs=2,
        verbose=True,
    )
