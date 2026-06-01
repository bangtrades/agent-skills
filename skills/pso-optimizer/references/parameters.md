# PSO Parameters: Complete Analysis

## Table of Contents
1. [Inertia Weight (w)](#inertia-weight)
2. [Acceleration Coefficients (c1, c2)](#acceleration-coefficients)
3. [Constriction Factor](#constriction-factor)
4. [Velocity Clamping](#velocity-clamping)
5. [Swarm Size](#swarm-size)
6. [Parameter Interactions](#parameter-interactions)
7. [Stability Analysis](#stability-analysis)
8. [Adaptive Parameter Strategies](#adaptive-strategies)
9. [Meta-Optimization of Parameters](#meta-optimization)

---

## Inertia Weight (w) {#inertia-weight}

The inertia weight controls how much of the previous velocity carries forward. It was introduced by Shi and Eberhart in 1998 to replace the original velocity clamping mechanism.

### Role and Effect

- **High w (> 0.8)**: Particles maintain momentum, encouraging exploration of new regions
- **Low w (< 0.4)**: Particles decelerate quickly, focusing search around current attractors (exploitation)
- **w >= 1**: Velocities grow unboundedly (divergence/explosion)
- **w = 0**: No momentum; particles jump directly based on cognitive and social pulls

### Constant Inertia Weight

The simplest approach. Common values:
- w = 0.7298 (derived from constriction factor with phi = 4.1)
- w = 0.729 (rounded, widely used)
- w = 0.5 (conservative, exploitation-heavy)

### Linear Time-Varying Inertia Weight (LDIW)

The most popular adaptive scheme. Decreases w linearly over iterations:

```
w(t) = w_max - (w_max - w_min) * t / t_max
```

Typical values: w_max = 0.9, w_min = 0.4

Rationale: Start with broad exploration, gradually shift to fine-grained exploitation as the swarm narrows in on promising regions.

### Nonlinear Decay Strategies

**Power decay:**
```
w(t) = ((t_max - t) / t_max)^n * (w_max - w_min) + w_min
```
n > 1 gives slower initial decay (more exploration time), n < 1 gives faster initial decay.

**Exponential decay:**
```
w(t) = w_min + (w_max - w_min) * exp(-k * (t / t_max)^2)
```

**Logarithmic decay:**
```
w(t) = w_min + (w_max - w_min) * log(1 + (e-1) * (t_max - t) / t_max)
```

### Chaotic Inertia Weight

Uses a chaotic sequence (e.g., logistic map) for ergodic coverage:
```
z(t+1) = 4 * z(t) * (1 - z(t))       # Logistic map
w(t) = (w_max - w_min) * z(t) + w_min
```

Provides more diverse parameter exploration than deterministic schedules.

### Adaptive Inertia Weight (APSO)

Adjusts w based on an evolutionary factor computed from swarm state:

```
d_i = (1/(S-1)) * sum_j ||x_i - x_j||   # Mean distance of particle i to all others
d_g = d of the global best particle
ef = (d_g - d_min) / (d_max - d_min)      # Evolutionary factor in [0, 1]
w(ef) = 1 / (1 + 1.5 * exp(-2.6 * ef))   # Sigmoid mapping
```

The evolutionary factor classifies the swarm state as exploration, exploitation, convergence, or jumping-out, and adapts w accordingly.

### Random Inertia Weight

```
w(t) ~ Uniform(w_min, w_max)   # or
w(t) ~ N(0.7, 0.1)             # Gaussian around typical value
```

Simple stochastic approach that adds diversity to the search dynamics.

---

## Acceleration Coefficients (c1, c2) {#acceleration-coefficients}

### Cognitive Coefficient (c1)

Controls attraction toward the particle's own historical best position (personal memory).
- High c1: Particles trust their own experience more (individualistic search)
- Low c1: Particles rely more on social information

### Social Coefficient (c2)

Controls attraction toward the neighborhood's best position (social learning).
- High c2: Particles converge quickly toward the current best known solution
- Low c2: Swarm explores more independently

### Classic Values

- c1 = c2 = 2.0 (original Kennedy & Eberhart, 1995)
- c1 = c2 = 1.49618 (derived from constriction factor)
- c1 = 2.5, c2 = 0.5 -> 0.5, c2 = 2.5 (time-varying: start cognitive, end social)

### Time-Varying Acceleration Coefficients

A common strategy increases social attraction while decreasing cognitive attraction:

```
c1(t) = c1_initial - (c1_initial - c1_final) * t / t_max
c2(t) = c2_initial + (c2_final - c2_initial) * t / t_max
```

Typical: c1: 2.5 -> 0.5, c2: 0.5 -> 2.5

Rationale: Early iterations emphasize personal exploration, later iterations emphasize social convergence.

### Constraint: c1 + c2

- c1 + c2 < 4: Required for stability (without inertia weight or constriction)
- c1 + c2 > 4: Required for constriction factor to be defined (phi = c1 + c2)
- Typical: c1 + c2 = 4.1 (standard constriction factor setup)

---

## Constriction Factor {#constriction-factor}

Introduced by Clerc and Kennedy (2002) as a principled alternative to inertia weight + velocity clamping.

### Derivation

Starting from the velocity update without inertia weight:
```
v(t+1) = v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))
```

The constriction coefficient K is derived from stability analysis:
```
phi = c1 + c2 (must be > 4)
K = 2 / |2 - phi - sqrt(phi^2 - 4*phi)|
```

The constricted velocity update:
```
v(t+1) = K * [v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))]
```

### Standard Values

With phi = 4.1 (c1 = c2 = 2.05):
- K = 0.7298
- Effective c1 = K * 2.05 = 1.49618
- Effective c2 = K * 2.05 = 1.49618

### Equivalence with Inertia Weight

The constriction approach is equivalent to:
- w = K
- c1_effective = K * c1_original
- c2_effective = K * c2_original

The constriction approach is preferred because all parameters derive from a single constraint (phi > 4), rather than requiring independent tuning of w, c1, c2.

### Convergence Guarantee

With proper constriction, the particle system is guaranteed to converge (velocities approach zero). However, this only guarantees convergence to SOME point -- not necessarily the global optimum. The swarm may need stochastic perturbation or topology changes to escape local optima after convergence.

---

## Velocity Clamping {#velocity-clamping}

Limits the maximum velocity to prevent particles from overshooting the search space.

### Standard Approach

```
v_max,d = k * (ub_d - lb_d)   where k in (0, 1]
```

Common choices:
- k = 1.0 (v_max equals the range of the search space per dimension)
- k = 0.5 (more conservative)
- k = 0.1 (very restrictive, for fine-grained search)

### With Constriction Factor

When using the constriction factor, velocity clamping is theoretically unnecessary because the constriction guarantees convergence. In practice, some implementations still apply a loose v_max as a safety measure, especially during early iterations when velocities can be large.

### Adaptive Velocity Clamping

```
v_max(t) = v_max_initial * (1 - t/t_max)^alpha
```

Reduces maximum velocity over time, matching the transition from exploration to exploitation.

---

## Swarm Size {#swarm-size}

### Guidelines

- **Small problems (< 10D)**: 20-30 particles
- **Medium problems (10-30D)**: 30-50 particles
- **Large problems (30-100D)**: 50-100 particles
- **Very large problems (> 100D)**: 100+ particles, or use decomposition

SPSO-2011 default: 40 particles.

### Swarm Size vs Iterations Tradeoff

Given a fixed budget of N function evaluations:
- More particles + fewer iterations = better exploration, worse exploitation
- Fewer particles + more iterations = worse exploration, better exploitation

For expensive objective functions, prefer fewer particles with more iterations. For cheap functions with many local optima, prefer more particles.

### Dynamic Population Sizing

Some approaches vary swarm size during optimization:
- Start large for exploration, reduce for exploitation
- Split/merge subswarms based on diversity metrics
- TRIBES: Self-adapting population size based on performance

---

## Parameter Interactions {#parameter-interactions}

Parameters do not act independently. Key interactions:

### w and c1 + c2

The stability region in (w, c1+c2) space is bounded by:
- w > 0
- c1 + c2 > 0
- w > (c1 + c2)/2 - 1

Within this region, the particle trajectory converges. Outside it, velocities diverge.

### Exploration-Exploitation Balance

| Configuration | Effect |
|--------------|--------|
| High w, low c1+c2 | Broad exploration, slow convergence |
| Low w, high c2 | Fast exploitation, risk of premature convergence |
| High c1, low c2 | Individualistic search, poor social learning |
| Low c1, high c2 | Social convergence, particles follow the leader |
| Balanced | Typically best for unknown problems |

### Sensitivity Analysis

Empirical studies show parameter sensitivity ranking:
1. **w** (most sensitive) - small changes significantly affect behavior
2. **c1 + c2 ratio** - affects exploration/exploitation balance
3. **Swarm size** - diminishing returns beyond ~50 for most problems
4. **v_max** - mainly important without constriction factor

---

## Stability Analysis {#stability-analysis}

### Deterministic Analysis (Simplified)

Treating r1, r2 as constants, the particle update forms a linear recurrence:

```
[x(t+1)]   [1-c1*r1-c2*r2    w  ] [x(t)]   [c1*r1*p + c2*r2*g]
[v(t+1)] = [-c1*r1-c2*r2    w  ] [v(t)] + [c1*r1*p + c2*r2*g]
```

Stability requires the eigenvalues of the transition matrix to have magnitude < 1.

### Stochastic Analysis

The full stochastic system requires analyzing expectations and variances. Key results:
- E[v(t)] -> 0 as t -> infinity when stability conditions are met
- Var[x(t)] converges to a finite value (particles oscillate around the attractor)
- The attractor point is: x* = (c1*p + c2*g) / (c1 + c2)

### Lyapunov Stability

Poli and Langdon showed stability using Markov chain analysis of transition probabilities. Convergence requires eigenvalues of the expected transition matrix to lie within the unit circle.

---

## Adaptive Parameter Strategies {#adaptive-strategies}

### ADIWACO (2024)

Simultaneously adapts w, c1, and c2 based on swarm state metrics:
- Tracks improvement rate, diversity, and velocity dispersion
- Uses fuzzy logic rules to adjust all three parameters
- Outperforms fixed and linearly varying approaches on CEC benchmarks

### Self-Adaptive PSO

Each particle carries its own parameter set (w_i, c1_i, c2_i) which evolve alongside the solution:
- Good parameters lead to good solutions which lead to parameter propagation
- Similar to self-adaptation in evolution strategies

### Reinforcement Learning-Based Adaptation

Emerging approach where an RL agent learns to adjust PSO parameters based on swarm state features (diversity, improvement rate, iteration number).

---

## Meta-Optimization {#meta-optimization}

Using another optimizer to tune PSO's own parameters for a specific problem class:

1. Define a meta-objective: average PSO performance across a set of training problems
2. Use an outer optimizer (another PSO, Bayesian optimization, grid search) to tune w, c1, c2, S
3. Evaluate each parameter set by running PSO multiple times (due to stochasticity)

This is computationally expensive but useful when PSO will be applied repeatedly to similar problems (e.g., daily portfolio rebalancing).
