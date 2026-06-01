# PSO Implementation Guide

## Table of Contents
1. [Standard PSO in Python](#standard-python)
2. [Initialization Strategies](#initialization)
3. [Boundary Handling](#boundary)
4. [Stopping Criteria](#stopping)
5. [Parallel Evaluation](#parallel)
6. [Debugging PSO](#debugging)
7. [Libraries and Frameworks](#libraries)
8. [Benchmarking Your Implementation](#benchmarking)

---

## Standard PSO in Python {#standard-python}

### Minimal Implementation Pattern

```python
import numpy as np

class PSO:
    def __init__(self, objective_fn, bounds, n_particles=40,
                 w=0.7298, c1=1.49618, c2=1.49618, max_iter=1000):
        self.f = objective_fn
        self.bounds = np.array(bounds)  # shape (n_dims, 2): [[lb, ub], ...]
        self.n_dims = len(bounds)
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter

    def optimize(self):
        lb = self.bounds[:, 0]
        ub = self.bounds[:, 1]
        
        # Initialize positions uniformly within bounds
        positions = lb + (ub - lb) * np.random.rand(self.n_particles, self.n_dims)
        
        # Initialize velocities
        velocity_range = ub - lb
        velocities = -velocity_range + 2 * velocity_range * np.random.rand(
            self.n_particles, self.n_dims)
        
        # Evaluate initial fitness
        fitness = np.array([self.f(p) for p in positions])
        
        # Personal bests
        pbest_pos = positions.copy()
        pbest_fit = fitness.copy()
        
        # Global best
        gbest_idx = np.argmin(fitness)
        gbest_pos = positions[gbest_idx].copy()
        gbest_fit = fitness[gbest_idx]
        
        # Main loop
        for t in range(self.max_iter):
            r1 = np.random.rand(self.n_particles, self.n_dims)
            r2 = np.random.rand(self.n_particles, self.n_dims)
            
            # Update velocities
            cognitive = self.c1 * r1 * (pbest_pos - positions)
            social = self.c2 * r2 * (gbest_pos - positions)
            velocities = self.w * velocities + cognitive + social
            
            # Velocity clamping
            v_max = velocity_range
            velocities = np.clip(velocities, -v_max, v_max)
            
            # Update positions
            positions = positions + velocities
            
            # Boundary handling (absorb)
            positions = np.clip(positions, lb, ub)
            # Zero velocity for dimensions that hit bounds
            at_boundary = (positions == lb) | (positions == ub)
            velocities[at_boundary] = 0
            
            # Evaluate fitness
            fitness = np.array([self.f(p) for p in positions])
            
            # Update personal bests
            improved = fitness < pbest_fit
            pbest_pos[improved] = positions[improved]
            pbest_fit[improved] = fitness[improved]
            
            # Update global best
            best_idx = np.argmin(pbest_fit)
            if pbest_fit[best_idx] < gbest_fit:
                gbest_pos = pbest_pos[best_idx].copy()
                gbest_fit = pbest_fit[best_idx]
        
        return gbest_pos, gbest_fit
```

### Usage Example

```python
# Rastrigin function (a classic multimodal benchmark)
def rastrigin(x):
    return 10 * len(x) + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

bounds = [(-5.12, 5.12)] * 10  # 10 dimensions
pso = PSO(rastrigin, bounds, n_particles=50, max_iter=2000)
best_pos, best_fit = pso.optimize()
print(f"Best fitness: {best_fit:.6f}")  # Should approach 0.0
```

### Adding Linear Inertia Weight Decay

```python
# Inside the loop, replace fixed w:
w_max, w_min = 0.9, 0.4
w = w_max - (w_max - w_min) * t / self.max_iter
velocities = w * velocities + cognitive + social
```

### Adding Local (Ring) Topology

```python
# Replace global best with neighborhood best
def get_ring_best(self, i, pbest_pos, pbest_fit):
    """Ring topology: each particle has 2 neighbors by index."""
    S = self.n_particles
    neighbors = [(i - 1) % S, i, (i + 1) % S]
    best_neighbor = min(neighbors, key=lambda j: pbest_fit[j])
    return pbest_pos[best_neighbor]

# In the update loop, replace gbest_pos with per-particle neighborhood best:
for i in range(self.n_particles):
    nbest = self.get_ring_best(i, pbest_pos, pbest_fit)
    cognitive = self.c1 * r1[i] * (pbest_pos[i] - positions[i])
    social = self.c2 * r2[i] * (nbest - positions[i])
    velocities[i] = self.w * velocities[i] + cognitive + social
```

### Adding Constriction Factor

```python
# Replace inertia weight with constriction
phi = c1 + c2  # Must be > 4
K = 2.0 / abs(2.0 - phi - np.sqrt(phi**2 - 4*phi))
velocities = K * (velocities + cognitive + social)  # Note: no separate w
```

---

## Initialization Strategies {#initialization}

### Uniform Random (Default)

```python
positions = lb + (ub - lb) * np.random.rand(n_particles, n_dims)
```

Simple but may leave gaps in high dimensions.

### Latin Hypercube Sampling (Recommended)

Ensures better space coverage:

```python
from scipy.stats import qmc

sampler = qmc.LatinHypercube(d=n_dims)
sample = sampler.random(n=n_particles)  # Values in [0, 1]
positions = lb + (ub - lb) * sample
```

### Sobol Sequence

Even more uniform than LHS:

```python
sampler = qmc.Sobol(d=n_dims)
sample = sampler.random(n=n_particles)
positions = lb + (ub - lb) * sample
```

### Opposition-Based Initialization

Generate particles and their "opposites" to double coverage:

```python
positions = lb + (ub - lb) * np.random.rand(n_particles // 2, n_dims)
opposites = lb + ub - positions
positions = np.vstack([positions, opposites])
```

### Velocity Initialization

Options:
- **Zero velocity**: v = 0. Safe, but may slow initial exploration.
- **Random velocity**: v ~ Uniform(-(ub-lb), (ub-lb)). Standard approach.
- **Small random**: v ~ Uniform(-0.1*(ub-lb), 0.1*(ub-lb)). Conservative start.

Zero velocity is increasingly popular as it avoids early explosion and the inertia weight / constriction handles the exploration.

---

## Boundary Handling {#boundary}

### Absorb (Clamp)

```python
positions = np.clip(positions, lb, ub)
velocities[positions == lb] = 0  # Zero velocity at boundary
velocities[positions == ub] = 0
```

Most common. Simple and effective.

### Reflect

```python
for d in range(n_dims):
    below = positions[:, d] < lb[d]
    above = positions[:, d] > ub[d]
    positions[below, d] = 2 * lb[d] - positions[below, d]
    positions[above, d] = 2 * ub[d] - positions[above, d]
    velocities[below, d] *= -1
    velocities[above, d] *= -1
    # Clip again in case reflection overshoots
    positions[:, d] = np.clip(positions[:, d], lb[d], ub[d])
```

### Random Reinitialize

```python
out_of_bounds = (positions < lb) | (positions > ub)
random_pos = lb + (ub - lb) * np.random.rand(*positions.shape)
positions = np.where(out_of_bounds, random_pos, positions)
velocities[out_of_bounds] = 0  # Reset velocity for reinitialized dims
```

### Periodic (Wrap)

```python
for d in range(n_dims):
    range_d = ub[d] - lb[d]
    positions[:, d] = lb[d] + (positions[:, d] - lb[d]) % range_d
```

---

## Stopping Criteria {#stopping}

### Maximum Evaluations

```python
if total_evaluations >= max_evaluations:
    break
```

The most reliable criterion. Ensures deterministic computational budget.

### Fitness Threshold

```python
if gbest_fit <= target_fitness:
    break
```

Use when the optimal value is known (benchmarks) or a "good enough" threshold exists.

### Stagnation Detection

```python
stagnation_counter = 0
stagnation_limit = 50  # iterations without improvement

if improved_global_best:
    stagnation_counter = 0
else:
    stagnation_counter += 1

if stagnation_counter >= stagnation_limit:
    break  # or trigger diversification
```

### Diversity Threshold

```python
diversity = np.mean(np.std(positions, axis=0))
if diversity < diversity_threshold:
    break  # Swarm has converged
```

### Combined Criteria

```python
if (t >= max_iter or 
    gbest_fit <= target or 
    stagnation >= stagnation_limit or
    diversity < div_threshold):
    break
```

---

## Parallel Evaluation {#parallel}

### Python multiprocessing

```python
from multiprocessing import Pool

with Pool(processes=n_cores) as pool:
    fitness = pool.map(objective_fn, [positions[i] for i in range(n_particles)])
fitness = np.array(fitness)
```

### joblib (simpler API)

```python
from joblib import Parallel, delayed

fitness = np.array(
    Parallel(n_jobs=n_cores)(
        delayed(objective_fn)(positions[i]) for i in range(n_particles)
    )
)
```

### Asynchronous PSO

Update particles as soon as their evaluation finishes, rather than waiting for the full generation:

```python
import concurrent.futures

with concurrent.futures.ProcessPoolExecutor(max_workers=n_cores) as executor:
    futures = {
        executor.submit(objective_fn, positions[i]): i 
        for i in range(n_particles)
    }
    for future in concurrent.futures.as_completed(futures):
        i = futures[future]
        fitness[i] = future.result()
        # Update personal/global best immediately
        update_bests(i)
        # Update this particle's velocity/position immediately
        update_particle(i)
```

Asynchronous PSO is more complex but better utilizes parallel resources when evaluation times vary.

---

## Debugging PSO {#debugging}

### Common Issues and Diagnostics

**Particles cluster prematurely (premature convergence)**:
- Monitor diversity: `np.mean(np.std(positions, axis=0))`
- If diversity drops rapidly in early iterations, try: larger swarm, local topology, higher w, mutation

**Fitness not improving**:
- Check that personal/global best updates are correct (common bug: updating with worse fitness)
- Verify boundary handling doesn't trap particles
- Print best fitness every N iterations to verify progress

**Velocities exploding**:
- Check w < 1 (must be strictly less than 1)
- Verify constriction factor is applied correctly
- Add velocity clamping as safety net

**NaN or Inf in positions/velocities**:
- Add `np.isfinite()` checks after objective evaluation
- Handle Inf/NaN fitness by assigning worst possible value

### Visualization (2D problems)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# Plot fitness landscape
X, Y = np.meshgrid(np.linspace(lb[0], ub[0], 100),
                    np.linspace(lb[1], ub[1], 100))
Z = np.array([[objective_fn([x, y]) for x in X[0]] for y in Y[:, 0]])
ax.contourf(X, Y, Z, levels=50, cmap='viridis')

# Plot particles
ax.scatter(positions[:, 0], positions[:, 1], c='red', s=20, label='Particles')
ax.scatter(gbest_pos[0], gbest_pos[1], c='yellow', s=100, marker='*', label='Global Best')
ax.legend()
plt.show()
```

### Convergence Curve

```python
history = []
for t in range(max_iter):
    # ... PSO update ...
    history.append(gbest_fit)

plt.plot(history)
plt.xlabel('Iteration')
plt.ylabel('Best Fitness')
plt.yscale('log')  # If fitness spans orders of magnitude
plt.title('PSO Convergence')
plt.show()
```

---

## Libraries and Frameworks {#libraries}

### Python Libraries

| Library | Strengths | Notes |
|---------|-----------|-------|
| **pyswarm** | Simple, lightweight | Basic PSO only, good for quick experiments |
| **pyswarms** | Full-featured, visualization | Multiple topologies, plotters, extensible |
| **pymoo** | Multi-objective, constraints | MOPSO, NSGA-II, benchmarks included |
| **DEAP** | Evolutionary framework | PSO as one of many algorithms, flexible |
| **scipy.optimize** | N/A | No built-in PSO but `differential_evolution` is available |
| **optuna** | Bayesian + CMA-ES | Not PSO but good comparison baseline |
| **pagmo/pygmo** | Island model parallelism | C++ backend, excellent for large-scale |

### pyswarms Example

```python
import pyswarms as ps

options = {'c1': 1.49618, 'c2': 1.49618, 'w': 0.7298}
optimizer = ps.single.GlobalBestPSO(
    n_particles=40, dimensions=10, options=options,
    bounds=(lb_array, ub_array)
)
best_cost, best_pos = optimizer.optimize(objective_fn, iters=1000)
```

### pymoo Example (Multi-Objective)

```python
from pymoo.algorithms.moo.pso import MOPSO
from pymoo.optimize import minimize
from pymoo.problems import get_problem

problem = get_problem("zdt1")
algorithm = MOPSO(pop_size=100)
res = minimize(problem, algorithm, ('n_gen', 200), seed=1)
```

---

## Benchmarking Your Implementation {#benchmarking}

### Standard Test Functions

Always validate your PSO implementation on known benchmarks before applying to real problems:

| Function | Dims | Optimum | Properties |
|----------|------|---------|------------|
| Sphere | any | 0 at origin | Unimodal, separable |
| Rosenbrock | any | 0 at (1,...,1) | Unimodal, non-separable, valley |
| Rastrigin | any | 0 at origin | Multimodal, separable |
| Ackley | any | 0 at origin | Multimodal, non-separable |
| Griewank | any | 0 at origin | Multimodal, non-separable |
| Schwefel | any | 0 at ~420.97 | Multimodal, deceptive |

### What to Report

- **Best fitness** found (mean +/- std over 30+ independent runs)
- **Convergence curve** (best fitness vs iteration/evaluation)
- **Success rate** (% of runs achieving target fitness within budget)
- **Total function evaluations** to reach target
- **Wall-clock time** (especially if parallelized)

### CEC Benchmark Suites

For rigorous comparison with the literature:
- CEC 2014: 30 functions, shifted and rotated
- CEC 2017: Updated set with improved difficulty scaling
- CEC 2022: Latest suite with additional constraints

These are available via the `cec2017` Python package or opfunu library.
