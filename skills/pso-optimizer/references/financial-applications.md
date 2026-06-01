# PSO in Financial Markets and Trading

## Table of Contents
1. [Why PSO for Finance](#why-pso)
2. [Trading Strategy Optimization](#strategy-optimization)
3. [Portfolio Optimization](#portfolio)
4. [Technical Indicator Optimization](#indicators)
5. [Feature Selection for ML Models](#feature-selection)
6. [Risk Management](#risk)
7. [Practical Considerations](#practical)
8. [Walk-Forward Framework](#walk-forward)

---

## Why PSO for Finance {#why-pso}

Financial optimization problems are a natural fit for PSO because:

1. **Non-convex landscapes**: Trading strategy fitness surfaces have many local optima (different parameter combinations that work in different regimes)
2. **No gradients available**: Backtest performance is not differentiable with respect to strategy parameters
3. **Noisy evaluation**: Financial returns are stochastic; the same parameters may produce different results
4. **Mixed parameter types**: Strategies often mix continuous (stop-loss levels), integer (lookback periods), and categorical (indicator type) parameters
5. **Multi-objective nature**: Traders care about return, risk, drawdown, win rate, etc. simultaneously
6. **Computational budget**: Backtests are expensive; PSO converges with relatively few evaluations compared to grid search

### PSO vs Other Optimizers for Trading

| Method | Pros | Cons |
|--------|------|------|
| Grid Search | Exhaustive, reproducible | Exponential in dimensions, wasteful |
| Random Search | Simple, parallelizable | No learning, no convergence |
| Bayesian Opt | Sample-efficient, surrogate model | Struggles > 20D, expensive overhead |
| Genetic Algorithm | Good for discrete params, crossover | More parameters to tune, slower |
| **PSO** | Fast convergence, few params, intuitive | Can premature converge, rotation variant |
| Differential Evolution | Rotation invariant, robust | Slower than PSO on smooth landscapes |

---

## Trading Strategy Optimization {#strategy-optimization}

### Problem Formulation

A trading strategy has parameters theta = (theta_1, ..., theta_n) that determine entry/exit signals. The optimization problem:

```
maximize  f(theta) = Performance_metric(backtest(strategy, theta, data))
subject to theta_lb <= theta <= theta_ub
```

### Encoding Strategy Parameters as Particles

Each particle position represents a complete strategy configuration:

```
Example for a dual-MA crossover + RSI filter strategy:
  Particle = [fast_MA_period, slow_MA_period, RSI_period, RSI_oversold, RSI_overbought, stop_loss_pct, take_profit_pct]
  Bounds   = [5, 20, 5, 15, 65, 0.5, 1.0] to [50, 200, 30, 40, 85, 5.0, 10.0]
```

For integer parameters (like MA periods), round after the position update:
```
x_int = round(x_continuous)
```

Or use the "round-on-evaluation" approach: keep positions continuous but round when passing to the backtest function.

### Fitness Functions

Choose the fitness function carefully -- it determines what PSO optimizes for:

**Sharpe Ratio** (most common):
```
f(theta) = mean(returns) / std(returns) * sqrt(252)
```
Balances return and risk. Penalizes inconsistent strategies.

**Sortino Ratio** (asymmetric risk):
```
f(theta) = mean(returns) / std(negative_returns) * sqrt(252)
```
Only penalizes downside volatility.

**Calmar Ratio**:
```
f(theta) = annualized_return / max_drawdown
```
Directly targets drawdown control.

**Profit Factor**:
```
f(theta) = sum(winning_trades) / abs(sum(losing_trades))
```

**Composite Fitness** (recommended for robustness):
```
f(theta) = w1 * sharpe + w2 * (1 - max_drawdown/max_allowed_dd) + w3 * profit_factor
```

### Overfitting Prevention

The biggest risk in strategy optimization is overfitting to historical data. Mitigation strategies:

1. **Walk-forward optimization**: See dedicated section below
2. **Out-of-sample validation**: Split data into train/validate/test
3. **Parameter stability penalty**: Penalize parameters in extreme regions of their range
4. **Robustness testing**: Evaluate on perturbed parameters (Monte Carlo around solution)
5. **Minimum trade count**: Reject strategies with too few trades in the backtest
6. **Cross-validation on time periods**: K-fold on non-overlapping time windows

---

## Portfolio Optimization {#portfolio}

### Mean-Variance Optimization

Classic Markowitz problem:

```
minimize  w^T * Sigma * w                    (portfolio variance)
subject to w^T * mu >= target_return          (return constraint)
           sum(w) = 1                          (fully invested)
           0 <= w_i <= max_weight              (position limits)
```

Where w is the weight vector, Sigma is the covariance matrix, mu is expected returns.

PSO particle: w = [w_1, w_2, ..., w_n] (asset weights)
Normalization: after each update, normalize weights to sum to 1.

### Multi-Objective Portfolio (MOPSO)

More realistic formulation using Pareto optimization:

```
minimize  [portfolio_variance(w), -portfolio_return(w), max_drawdown(w)]
subject to sum(w) = 1, w >= 0
```

Each particle's personal best and archive selection use Pareto dominance.

### PSO Advantages for Portfolio

- Handles non-convex constraints (cardinality constraints, minimum lot sizes)
- No assumption of normal returns (works with any risk metric)
- Naturally incorporates transaction costs as part of the fitness evaluation
- Can optimize non-standard risk measures (CVaR, drawdown) that lack closed-form gradients

### Risk Parity with PSO

Optimize weights so each asset contributes equally to portfolio risk:

```
minimize  sum_i (w_i * (Sigma * w)_i / (w^T * Sigma * w) - 1/n)^2
```

This is non-convex and non-smooth -- perfect for PSO.

---

## Technical Indicator Optimization {#indicators}

### Simultaneous Indicator + Rule Optimization

Recent research (2024) uses PSO to jointly optimize:
1. Indicator parameters (EMA period, RSI lookback, Bollinger Band width)
2. Trading rule definitions (threshold levels for entry/exit)
3. Signal aggregation weights (how to combine multiple indicators)

### Particle Encoding for Multi-Indicator System

```
Particle = [
  EMA_fast, EMA_slow,           # Moving average parameters
  RSI_period, RSI_buy, RSI_sell, # RSI parameters and thresholds
  BB_period, BB_std,             # Bollinger Band parameters
  MACD_fast, MACD_slow, MACD_signal, # MACD parameters
  w_EMA, w_RSI, w_BB, w_MACD    # Signal aggregation weights
]
```

The aggregation weights determine how strongly each indicator contributes to the final trading signal. PSO optimizes the entire system simultaneously, capturing interactions between indicators that sequential optimization would miss.

### Regime-Adaptive Optimization

Train different PSO-optimized parameter sets for different market regimes:
1. Classify market state (trending, mean-reverting, volatile, quiet)
2. Optimize separate parameter sets for each regime
3. Use a regime detector to switch between parameter sets in real-time

---

## Feature Selection for ML Models {#feature-selection}

### Binary PSO for Feature Selection

Use Binary PSO where each dimension represents include/exclude decision for a feature:

```
Particle = [1, 0, 1, 1, 0, ...]  # 1 = include feature, 0 = exclude
```

Fitness function: cross-validated model performance with the selected features

```
f(particle) = cv_score(model, X[:, selected_features], y) - lambda * n_features / total_features
```

The penalty term prevents overfitting by preferring simpler feature sets.

### Wrapper Feature Selection for Trading Models

1. Define a pool of candidate features (technical indicators, fundamental data, sentiment scores, microstructure features)
2. Each particle selects a subset of features
3. Train a prediction model (random forest, LSTM, gradient boosting) using selected features
4. Evaluate on out-of-sample data
5. Fitness = prediction accuracy or trading P&L

---

## Risk Management {#risk}

### VaR Optimization

Use PSO to find portfolio weights that minimize Value-at-Risk:

```
minimize  VaR_alpha(portfolio_returns(w))
subject to E[portfolio_return(w)] >= target, sum(w) = 1
```

VaR has no analytical gradient for general return distributions, making PSO well-suited.

### CVaR (Expected Shortfall)

```
minimize  CVaR_alpha(w) = E[loss | loss > VaR_alpha]
```

More coherent than VaR and sub-additive (diversification always helps), but still non-smooth.

### Dynamic Hedging Optimization

Optimize hedge ratios for a portfolio using PSO:
```
Particle = [hedge_ratio_1, ..., hedge_ratio_k]  # For k hedging instruments
Fitness = -tracking_error(hedged_portfolio) - lambda * hedging_cost
```

---

## Practical Considerations {#practical}

### Handling Noisy Fitness

Financial backtests are noisy -- the same parameters may give different results depending on:
- Date range
- Data quality
- Execution assumptions (slippage, fill rates)

Strategies to handle noise:
1. **Average over multiple time periods**: f(theta) = mean(f_period_1, f_period_2, ..., f_period_k)
2. **Bootstrap resampling**: Evaluate the same strategy on bootstrap samples of the return series
3. **Larger swarm**: More particles means more robust exploration despite noise
4. **Conservative personal best update**: Only update p_i if the improvement exceeds a significance threshold

### Computational Optimization

Backtesting is the bottleneck. Speed strategies:
1. **Vectorized backtester**: Use numpy/pandas vectorized operations instead of looping through bars
2. **Parallel evaluation**: Each particle's backtest is independent -- run on multiple cores
3. **Caching**: Cache backtest results for repeated parameter combinations (especially with integer params that round to the same value)
4. **Surrogate model**: After initial PSO evaluations, fit a surrogate (Gaussian process, neural network) to approximate the fitness surface for preliminary screening

### PSO Parameters for Trading

Recommended settings for trading strategy optimization:
- **Swarm size**: 30-50 (more for higher-dimensional parameter spaces)
- **Topology**: Von Neumann or adaptive random (avoid gbest due to overfitting risk)
- **Inertia weight**: Linear decay 0.9 -> 0.4 over iterations
- **c1 = c2 = 1.5**: Slightly below standard to reduce premature convergence
- **Max iterations**: 100-500 (limited by backtest cost)
- **Multiple runs**: Run PSO 5-10 times with different random seeds, take the best result that also validates out-of-sample

---

## Walk-Forward Framework {#walk-forward}

Walk-forward optimization is the gold standard for strategy optimization to avoid overfitting.

### Basic Walk-Forward

```
For each window w in 1..W:
  train_data = data[w * step : w * step + train_length]
  test_data  = data[w * step + train_length : w * step + train_length + test_length]
  
  theta_w = PSO_optimize(strategy, train_data)  # Optimize on training window
  pnl_w = backtest(strategy, theta_w, test_data)  # Test on out-of-sample
  
out_of_sample_pnl = concat(pnl_1, pnl_2, ..., pnl_W)
```

### Anchored Walk-Forward

Training window always starts from the same date but expands:
```
train_data = data[0 : w * step + train_length]  # Growing window
```

More data for training as time progresses, but risks regime changes.

### PSO in Walk-Forward

Within each training window:
1. Run PSO to find optimal parameters
2. Evaluate the TOP 5-10 particles (not just the best) on validation data
3. Select the parameter set that performs best on validation
4. Apply to the out-of-sample test period

This "ensemble of good solutions" approach is more robust than taking the single PSO-best.

### Walk-Forward Efficiency Ratio

```
WFE = out_of_sample_return / in_sample_return
```

A WFE near 1.0 means the strategy generalizes well. WFE << 1.0 indicates overfitting.
Target: WFE > 0.5 as a minimum threshold.

### Warm-Starting PSO Across Windows

Use the best particles from window w as the initial swarm for window w+1:
- Keep 50% of particles from the previous window
- Reinitialize 50% randomly
- This leverages parameter continuity (optimal parameters usually don't change drastically between adjacent windows)
