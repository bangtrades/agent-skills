---
name: pso-optimizer
description: >
  Particle Swarm Optimization (PSO) skill for algorithm design, implementation, parameter tuning,
  convergence analysis, and variant selection. Trigger on: PSO, particle swarm, swarm intelligence,
  metaheuristic optimization, population-based optimization, gradient-free search, hyperparameter
  tuning, portfolio optimization, trading strategy optimization, feature selection, inertia weight,
  constriction factor, swarm topology, or comparisons with genetic algorithms / differential
  evolution. Also trigger when users describe optimizing black-box functions, tuning parameters
  without gradients, or finding global optima in rugged fitness landscapes.
---

# Particle Swarm Optimization (PSO) - Complete Reference

PSO is a population-based stochastic optimization algorithm inspired by the social behavior of bird flocking and fish schooling. Introduced by Kennedy and Eberhart in 1995, it optimizes a problem by iteratively improving candidate solutions (particles) that move through the search space guided by their own experience and the experience of their neighbors.

PSO's power comes from its simplicity, few hyperparameters, and ability to optimize non-differentiable, multimodal, and high-dimensional functions without requiring gradient information.

## When to Use PSO

PSO excels when:
- The objective function is non-differentiable, noisy, or has many local optima
- The search space is continuous (though discrete variants exist)
- You need a good solution quickly rather than a provably optimal one
- The problem has 2-100 dimensions (for higher dimensions, see Large-Scale section)
- Parallelization is important (particles evaluate independently)

PSO may not be ideal when:
- The problem is convex (use gradient-based methods instead)
- You need guaranteed global optimality (PSO is a metaheuristic)
- The dimensionality exceeds ~1000 without decomposition strategies
- The function is extremely cheap to evaluate (grid/random search may suffice)

## Core Algorithm

### Mathematical Formulation

Given an objective function f: R^n -> R to minimize, PSO maintains a swarm of S particles. Each particle i has:
- Position: x_i in R^n (a candidate solution)
- Velocity: v_i in R^n (direction and speed of movement)
- Personal best: p_i (best position this particle has found)
- Neighborhood best: g (best position found by the particle's neighborhood)

### Velocity and Position Update Equations

At each iteration t, for each particle i and dimension d:

```
v_i,d(t+1) = w * v_i,d(t) + c1 * r1 * (p_i,d - x_i,d(t)) + c2 * r2 * (g_d - x_i,d(t))
x_i,d(t+1) = x_i,d(t) + v_i,d(t+1)
```

Where:
- **w** (inertia weight): Controls momentum. Balances exploration (high w) vs exploitation (low w)
- **c1** (cognitive coefficient): Attraction toward particle's own best. Typically 1.5-2.0
- **c2** (social coefficient): Attraction toward neighborhood best. Typically 1.5-2.0
- **r1, r2**: Independent uniform random numbers in [0, 1], sampled per dimension per particle per iteration
- **p_i**: Personal best position of particle i
- **g**: Best position found by the neighborhood (global best or local best depending on topology)

The three velocity terms represent:
1. **Inertia** (w * v): Particle continues in its current direction
2. **Cognitive pull** (c1 * r1 * (p - x)): Particle returns toward its own best discovery
3. **Social pull** (c2 * r2 * (g - x)): Particle moves toward the best discovery of its peers

### Algorithm Pseudocode

```
INITIALIZE:
  For each particle i in 1..S:
    x_i ~ Uniform(lb, ub)                    # Random position in bounds
    v_i ~ Uniform(-(ub-lb), (ub-lb))         # Random velocity
    p_i = x_i                                 # Personal best = initial position
  g = argmin_i f(p_i)                         # Global/neighborhood best

ITERATE until stopping criterion:
  For each particle i:
    For each dimension d:
      r1, r2 ~ Uniform(0, 1)
      v_i,d = w * v_i,d + c1 * r1 * (p_i,d - x_i,d) + c2 * r2 * (g_d - x_i,d)
      v_i,d = clamp(v_i,d, -v_max, v_max)    # Optional velocity clamping
      x_i,d = x_i,d + v_i,d

    If f(x_i) < f(p_i):
      p_i = x_i                               # Update personal best
      If f(x_i) < f(g):
        g = x_i                               # Update neighborhood best

RETURN g
```

## Parameter Guide

For detailed mathematical analysis of all parameters, stability conditions, constriction coefficients, and advanced tuning strategies, read `references/parameters.md`.

### Quick-Start Parameters

For most problems, these defaults work well:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Swarm size (S) | 30-50 | 40 is the SPSO-2011 default |
| Inertia weight (w) | 0.7298 | Or linear decay 0.9 -> 0.4 |
| Cognitive coeff (c1) | 1.49618 | Derived from constriction factor |
| Social coeff (c2) | 1.49618 | Derived from constriction factor |
| v_max | range of search space | Per dimension |
| Max iterations | 1000-10000 | Problem dependent |

### Inertia Weight Strategies

1. **Constant**: w = 0.7298 (constriction-derived). Simple and often effective.
2. **Linear decay**: w(t) = w_max - (w_max - w_min) * t / t_max. Classic approach: 0.9 -> 0.4.
3. **Nonlinear decay**: w(t) = ((t_max - t) / t_max)^n * (w_min - w_max) + w_max
4. **Adaptive**: w(ef) = 1 / (1 + 1.5 * exp(-2.6 * ef)) where ef is evolutionary factor based on swarm diversity.
5. **Chaotic**: w from logistic map for ergodic coverage of the parameter space.

### Constriction Factor (Clerc & Kennedy)

An alternative to inertia weight that provides mathematical convergence guarantees:

```
K = 2 / |2 - phi - sqrt(phi^2 - 4*phi)|

where phi = c1 + c2 > 4 (typically phi = 4.1)
```

With phi = 4.1: K ~= 0.7298, and the standard coefficients become c1 = c2 = phi/2 * K ~= 1.49618.

The constriction approach and inertia weight are mathematically equivalent when w = K and c1, c2 are scaled by K. The constriction approach is preferred because it derives parameters from a single stability constraint rather than requiring independent tuning.

## Topologies

The topology defines which particles communicate with each other. This is one of the most impactful design choices in PSO.

### Global Best (gbest)
Every particle knows the best position found by the entire swarm. Fast convergence but prone to premature convergence on multimodal problems. Use for unimodal problems or when speed matters more than reliability.

### Local Best (lbest) / Ring Topology
Each particle communicates only with its k nearest neighbors (by index, not distance). Slower convergence but much better at avoiding local optima. k=2 (ring) is the classic choice. Use for multimodal problems.

### Von Neumann Topology
Particles arranged on a 2D grid, communicating with 4 neighbors (up/down/left/right). Empirically one of the best-performing static topologies, balancing convergence speed and diversity.

### SPSO-2011 Adaptive Random Topology
Each particle has a probability p of being connected to every other particle. Topology is regenerated when no improvement is found for a specified number of iterations. This is the state-of-the-art standard approach.

### Fully Informed Particle Swarm (FIPS)
Each particle is influenced by ALL its neighbors' personal bests, weighted by fitness:
```
p_i = sum(phi_k * p_k) / sum(phi_k) for all neighbors k
```
Eliminates the distinction between cognitive and social components.

For more topology details, mathematical properties, and selection guidance, see `references/topologies-and-variants.md`.

## PSO Variants

PSO has spawned many variants. Read `references/topologies-and-variants.md` for full coverage including:

- **Bare Bones PSO**: Samples from Gaussian distribution centered between personal and global best. No velocity needed.
- **Accelerated PSO (APSO)**: Velocity-free with exponential attraction and random perturbation.
- **Cooperative PSO (CPSO)**: Decomposes high-dimensional problems into 1-D subswarms.
- **Multi-Objective PSO (MOPSO)**: Uses Pareto dominance and external archives.
- **Discrete/Binary PSO**: For combinatorial optimization problems.
- **Guaranteed Convergence PSO (GCPSO)**: Addresses stagnation at global best position.
- **Competitive Swarm Optimizer (CSO)**: For large-scale optimization (1000+ dimensions).
- **Hybrid PSO-DE, PSO-GA, PSO-SA**: Combines PSO with other metaheuristics.

## Convergence Theory

Understanding convergence is important for parameter selection and knowing when PSO can be trusted.

### Two Types of Convergence

1. **Sequence convergence**: All particles converge to a single point (which may not be the global optimum). This is achievable with proper parameter settings.

2. **Optimum convergence**: The swarm's best known position approaches a local/global optimum. Standard PSO does NOT guarantee this without modification.

### Stability Conditions

For a single particle with deterministic coefficients, the system is stable (velocities converge to zero) when:
- 0 < c1 + c2 < 4
- 0 < w < 1
- w > (c1 + c2) / 2 - 1

The constriction factor automatically satisfies these conditions when phi > 4.

### Recent Theoretical Advances

- Huang et al. (2023) proved global convergence using stochastic differential equation formulations and mean-field analysis, establishing polynomial complexity bounds.
- Tong et al. (2021) proved almost sure convergence (probability 1) for modified PSO variants with sufficient stochasticity.
- Nigatu et al. (2024) analyzed convergence under different constriction factors using Markov chain analysis.

For full convergence analysis details, see `references/convergence-theory.md`.

## Practical Implementation

### Initialization

- **Positions**: Uniform random within search bounds
- **Velocities**: Uniform random in [-(ub-lb), (ub-lb)] or simply zero
- **Latin Hypercube Sampling**: Better space coverage than pure random for positions

### Boundary Handling

When particles leave the search space:
1. **Absorb**: Clamp position to boundary, zero out velocity in that dimension
2. **Reflect**: Bounce off boundary (reverse velocity component)
3. **Wrap**: Periodic boundary conditions
4. **Random reinitialize**: Place particle randomly within bounds

Absorb is the most common and works well for most problems.

### Stopping Criteria

- Maximum iterations/function evaluations reached
- Fitness threshold achieved
- Swarm diversity drops below threshold (all particles converged)
- No improvement for N consecutive iterations

### Common Pitfalls

1. **Premature convergence**: Swarm collapses to local optimum. Fix with: local topology, larger swarm, diversity maintenance, or mutation operators.
2. **Velocity explosion**: Particles fly out of bounds. Fix with: constriction factor, velocity clamping, or proper w < 1.
3. **Dimensional coupling**: Standard PSO has rotation variance (performance depends on coordinate alignment). Fix with: rotation-invariant updates (SPSO-2011) or coordinate rotation.
4. **Stagnation**: No progress near optimum. Fix with: GCPSO, perturbation operators, or adaptive topology reset.

## Financial & Trading Applications

PSO is particularly powerful for trading and financial optimization because these problems are typically non-convex, noisy, and have many local optima.

For detailed coverage of financial applications including portfolio optimization, trading strategy parameter tuning, indicator optimization, and risk management, see `references/financial-applications.md`.

### Key Use Cases

- **Strategy parameter optimization**: Optimize EMA periods, RSI thresholds, stop-loss/take-profit levels simultaneously
- **Portfolio allocation**: Multi-objective optimization of risk/return with constraints
- **Indicator signal aggregation**: Weight and combine multiple technical indicators
- **Feature selection**: Select optimal input features for ML trading models
- **Neural network training**: Optimize weights for price prediction models

## Implementation Reference

The `scripts/` directory contains ready-to-use implementations:

- `scripts/pso_core.py`: Standard PSO implementation with configurable topology, parameters, and boundary handling
- `scripts/pso_trading.py`: PSO adapted for trading strategy optimization with walk-forward validation

To implement PSO from scratch or adapt it to a specific problem, read `references/implementation-guide.md`.

## Quick Decision Tree

```
Is your problem differentiable and convex?
  YES -> Use gradient-based methods (Adam, L-BFGS, etc.)
  NO  -> Continue

Is your search space discrete/combinatorial?
  YES -> Consider Binary PSO or Discrete PSO variants
  NO  -> Continue

How many dimensions?
  < 30  -> Standard PSO with constriction factor
  30-100 -> PSO with Von Neumann or adaptive random topology
  100-1000 -> Cooperative PSO (CPSO) with subswarm decomposition
  > 1000 -> CSO or LLSO (large-scale variants)

Is it multi-objective?
  YES -> MOPSO with external archive
  NO  -> Continue

Is premature convergence an issue?
  YES -> Local topology + diversity maintenance + mutation
  NO  -> Global best topology for speed

Need parallelization?
  YES -> Ring topology enables generation-level parallelism
  NO  -> Any topology
```

## References and Further Reading

For deep dives into specific topics, the reference files are organized as:

| File | Contents |
|------|----------|
| `references/parameters.md` | Complete parameter analysis, stability math, tuning strategies |
| `references/topologies-and-variants.md` | All topologies, all major PSO variants with equations |
| `references/convergence-theory.md` | Mathematical convergence proofs, stability analysis |
| `references/financial-applications.md` | Trading, portfolio, risk management applications |
| `references/implementation-guide.md` | Step-by-step implementation guidance with Python patterns |

### Seminal Papers

- Kennedy & Eberhart (1995): Original PSO paper
- Shi & Eberhart (1998): Inertia weight introduction
- Clerc & Kennedy (2002): Constriction factor analysis
- Mendes et al. (2004): Fully Informed Particle Swarm
- Clerc (2012): SPSO-2011 specification
- Bonyadi & Michalewicz (2017): Comprehensive PSO analysis
