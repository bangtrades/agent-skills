# PSO Topologies and Variants: Complete Reference

## Table of Contents
1. [Topology Fundamentals](#topology-fundamentals)
2. [Static Topologies](#static-topologies)
3. [Dynamic Topologies](#dynamic-topologies)
4. [Standard PSO Variants](#standard-variants)
5. [Velocity-Free Variants](#velocity-free)
6. [Multi-Objective PSO](#mopso)
7. [Discrete and Binary PSO](#discrete-pso)
8. [Large-Scale Variants](#large-scale)
9. [Hybrid Approaches](#hybrids)
10. [Constrained Optimization](#constrained)
11. [Multimodal / Niching PSO](#multimodal)

---

## Topology Fundamentals {#topology-fundamentals}

The topology defines which particles share information. It is arguably the most important structural decision in PSO design because it controls the speed/reliability tradeoff of convergence.

**Key principle**: More connectivity = faster convergence but higher risk of premature convergence. Less connectivity = slower convergence but better global search.

### Terminology

- **Neighborhood**: The set of particles that influence a given particle's social component
- **Informant**: A particle whose personal best is available to the current particle
- **gbest**: Global best topology -- every particle is every other's neighbor
- **lbest**: Local best topology -- particles have a restricted neighborhood

---

## Static Topologies {#static-topologies}

### Global Best (Star / Fully Connected)

Every particle communicates with all others. The social component uses the single best position found by the entire swarm.

```
g = argmin_{j in 1..S} f(p_j)
```

- **Convergence speed**: Fastest
- **Premature convergence risk**: Highest
- **Best for**: Unimodal functions, small swarms, time-limited optimization
- **Equivalent**: lbest with neighborhood size = S

### Ring Topology (lbest, k=2)

Each particle i communicates with particles i-1 and i+1 (circular indexing). The social component uses the best among the particle and its two neighbors.

```
g_i = argmin f(p_j) for j in {i-1, i, i+1} mod S
```

- **Convergence speed**: Slowest of common topologies
- **Premature convergence risk**: Lowest
- **Best for**: Highly multimodal functions
- **Information propagation**: Takes O(S) iterations for information to traverse the swarm

### Von Neumann (Grid / Lattice)

Particles arranged on a 2D toroidal grid. Each particle communicates with 4 neighbors (up, down, left, right).

For a swarm of S = r * c particles:
```
Neighbors of particle at (row, col):
  (row-1, col), (row+1, col), (row, col-1), (row, col+1)  -- all mod r or c
```

- **Convergence speed**: Moderate
- **Premature convergence risk**: Moderate
- **Best for**: General purpose; empirically one of the best static topologies
- **Note**: Works best when S is a perfect square or near-square

### Wheel (Hub-and-Spoke)

One central particle connects to all others; peripheral particles connect only to the center.

- **Convergence speed**: Moderate
- **Properties**: Central particle acts as information filter, slowing premature convergence while maintaining some global communication
- **Risk**: Central particle becomes bottleneck

### Cluster / Hierarchical

Multiple fully-connected clusters with sparse inter-cluster connections.

```
Cluster 1: {p1, p2, p3} -- fully connected
Cluster 2: {p4, p5, p6} -- fully connected
Inter-cluster: p3 <-> p4
```

- **Properties**: Fast convergence within clusters, slow information transfer between clusters
- **Good for**: Multi-modal problems where different clusters can track different optima

---

## Dynamic Topologies {#dynamic-topologies}

### SPSO-2011 Adaptive Random Topology

The state-of-the-art standard. Each iteration where no global improvement occurs, the topology is regenerated:

1. Each particle i is always its own informant
2. For each other particle j, add a link i->j with probability p = 1 - (1 - 1/S)^K where K is typically 3
3. This gives each particle approximately K informants on average

When the global best improves, the topology is kept. When it stagnates, a new random topology is drawn. This creates an adaptive pressure: successful topologies persist, unsuccessful ones are replaced.

### Distance-Based Dynamic Topology

Neighborhood defined by spatial proximity:
```
N_i(t) = {j : ||x_i(t) - x_j(t)|| < r(t)}
```

Radius r(t) can be fixed or adaptive. Particles in dense regions share more information; isolated particles explore independently.

### Fitness-Distance-Ratio (FDR)

For each dimension d of particle i, select the neighbor that maximizes:
```
FDR_j,d = (f(p_i) - f(p_j)) / |p_i,d - p_j,d|
```

This selects informants that are both fitter and close in the relevant dimension, promoting efficient directed search.

### Small-World Networks

Based on Watts-Strogatz model: start with a ring topology, then rewire each connection with probability beta. Creates short average path lengths with clustering, combining benefits of local and global topologies.

### TRIBES

Self-adaptive topology and population size:
- Swarm organized into tribes (subswarms)
- Tribes grow by adding particles when performing poorly
- Tribes shrink by removing worst particles when performing well
- No user-defined parameters needed

---

## Standard PSO Variants {#standard-variants}

### Canonical PSO (1995)

The original Kennedy & Eberhart formulation without inertia weight:
```
v(t+1) = v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))
x(t+1) = x(t) + v(t+1)
```
Required velocity clamping (v_max) to prevent divergence.

### Inertia Weight PSO (1998)

Shi & Eberhart's modification adding momentum control:
```
v(t+1) = w*v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))
```
The w parameter made velocity clamping less critical and provided a principled exploration/exploitation control.

### Constriction PSO (2002)

Clerc & Kennedy's approach using mathematical stability analysis:
```
v(t+1) = K * [v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))]
K = 2 / |2 - phi - sqrt(phi^2 - 4*phi)|, phi = c1 + c2 > 4
```

### Fully Informed Particle Swarm (FIPS, 2004)

Mendes et al. replaced the single social attractor with a weighted combination of ALL neighbors' personal bests:

```
For particle i with neighbors N_i:
  chi = 4.1 / |N_i|  (distributed across neighbors)
  v(t+1) = K * [v(t) + sum_{j in N_i} chi * r_j * (p_j - x(t))]
```

- Eliminates the gbest/pbest distinction
- Each neighbor contributes equally (or weighted by fitness)
- Often performs better than standard PSO on multimodal problems

### Guaranteed Convergence PSO (GCPSO)

Van den Bergh's fix for stagnation when a particle IS the global best:

For the global best particle only:
```
v_gb(t+1) = -x_gb(t) + g + w*v_gb(t) + rho(t) * (1 - 2*r)
```

The search diameter rho(t) adapts:
- rho doubles after sc consecutive successes (expanding search)
- rho halves after fc consecutive failures (contracting search)
- Default: sc = 15, fc = 5

---

## Velocity-Free Variants {#velocity-free}

### Bare Bones PSO (Kennedy, 2003)

Eliminates velocity entirely. Position sampled from Gaussian:
```
x_i(t+1) ~ N(mu, sigma)
where:
  mu = (p_i + g) / 2
  sigma = |p_i - g|
```

The Gaussian is centered between personal and global best, with spread proportional to the distance between them. As the particle converges, sigma shrinks automatically.

### Modified Bare Bones PSO

Adds a probability of returning to personal best:
```
if r < 0.5:
  x_i(t+1) ~ N((p_i + g) / 2, |p_i - g|)
else:
  x_i(t+1) = p_i
```

### Accelerated PSO (APSO)

Position-only update with exponential attraction:
```
x_i(t+1) = (1 - beta) * x_i(t) + beta * g + alpha * L * u
```

Where:
- beta in [0.1, 0.7]: attraction strength to global best
- alpha in [0.1, 0.5]: random perturbation scale (can decay: alpha_n = alpha_0 * gamma^n)
- L: characteristic length scale of the problem
- u ~ Uniform(-1, 1) per dimension

Simpler than standard PSO and often faster convergence for unimodal problems.

---

## Multi-Objective PSO (MOPSO) {#mopso}

### Core Concepts

In multi-objective optimization, there's no single "best" solution. Instead, PSO must find the Pareto front -- the set of non-dominated solutions.

### Architecture

```
External Archive: stores non-dominated solutions found so far
Leader Selection: chooses a guide from the archive for each particle
Archive Maintenance: prunes archive when it exceeds capacity
```

### Leader Selection Strategies

1. **Crowding distance**: Select leaders from sparse regions of the Pareto front to promote diversity
2. **Random from archive**: Simple, avoids bias
3. **Sigma method**: Project objectives onto a sigma vector, match particles to closest archive member
4. **Angle-based**: Select leader maximizing angle diversity in objective space

### Archive Management

- **Epsilon-dominance**: Divide objective space into grid cells; keep one solution per cell
- **Crowding distance pruning**: Remove solutions in crowded regions first
- **Size-double mechanism**: Maintain separate archives for convergence and diversity

### MOPSO Velocity Update

```
v(t+1) = w*v(t) + c1*r1*(p_i - x(t)) + c2*r2*(leader - x(t))
```

Where `leader` is selected from the external archive rather than being a single global best.

### Performance Metrics

- **Hypervolume (HV)**: Volume of objective space dominated by the Pareto front (higher = better)
- **Generational Distance (GD)**: Average distance from found front to true front
- **Spread**: Uniformity of distribution along the Pareto front
- **Inverted GD (IGD)**: Combines convergence and diversity in one metric

---

## Discrete and Binary PSO {#discrete-pso}

### Binary PSO (Kennedy & Eberhart, 1997)

For binary decision variables, velocity is interpreted as probability via sigmoid:

```
v(t+1) = w*v(t) + c1*r1*(p - x(t)) + c2*r2*(g - x(t))
sigmoid(v) = 1 / (1 + exp(-v))
x(t+1) = 1 if r < sigmoid(v(t+1)), else 0
```

### Set-Based PSO

For combinatorial problems, operators are redefined:
- **Subtraction** (p - x): set difference indicating elements to add/remove
- **Multiplication** (c * set): probabilistic application of changes
- **Addition** (set1 + set2): union of change sets

### Discrete PSO for Permutations

For TSP-like problems, velocity becomes a sequence of swap operations:
```
v = [(i,j), (k,l), ...]  # List of position swaps
```

---

## Large-Scale Variants {#large-scale}

For problems with 100-10000+ dimensions, standard PSO suffers from the curse of dimensionality.

### Cooperative PSO (CPSO-S, van den Bergh 2004)

Decomposes an n-dimensional problem into n one-dimensional subproblems:

1. Create n subswarms, each optimizing one dimension
2. To evaluate particle i of subswarm k, construct a context vector using the global best of all other subswarms
3. Evaluate the full solution using this context vector

Trade-off: Assumes separability or weak interaction between dimensions. For non-separable problems, use CPSO-H which mixes 1-D and full-D subswarms.

### Competitive Swarm Optimizer (CSO)

For 1000+ dimensions:
1. Randomly pair particles in the swarm
2. The loser of each pair learns from the winner:
   ```
   v_loser(t+1) = r1*v_loser(t) + r2*(x_winner - x_loser) + r3*phi*(x_mean - x_loser)
   ```
3. Winners pass through unchanged (no personal/global best tracking)

CSO maintains diversity better than standard PSO in high dimensions because only losers update.

### Level-Based Learning Swarm Optimizer (LLSO)

Sorts particles by fitness into levels, each particle learns from a random particle in a better level:
```
x_i,d(t+1) = x_i,d(t) + r * (x_exemplar,d - x_i,d(t))
```
Where exemplar is from a demonstrably better level.

### Random Grouping with Cooperative Coevolution

1. Randomly partition dimensions into groups of size m
2. Optimize each group with a separate PSO subswarm
3. Re-partition periodically to capture cross-group interactions

---

## Hybrid Approaches {#hybrids}

### PSO + Differential Evolution (PSO-DE / DEPSO)

Alternates PSO and DE operations:
```
With probability p_de:
  Apply DE mutation: u = x_r1 + F*(x_r2 - x_r3)
  Apply DE crossover: trial vector from u and x_i
  Selection: keep trial if better than x_i
Otherwise:
  Apply standard PSO update
```

DE adds rotation-invariant exploration that PSO lacks.

### PSO + Genetic Algorithm (PSO-GA)

After PSO update, apply GA operators:
```
Selection: tournament or roulette based on fitness
Crossover: arithmetic crossover between pairs
  x_child = r * x_parent1 + (1-r) * x_parent2
Mutation: Gaussian perturbation with small probability
```

### PSO + Simulated Annealing (PSO-SA)

Apply SA acceptance criterion to personal best updates:
```
If f(x_new) < f(p_i):
  p_i = x_new  # Always accept improvements
Else:
  Accept with probability exp(-(f(x_new) - f(p_i)) / T(t))
```

Temperature T decreases over iterations. Allows temporary acceptance of worse solutions to escape local optima.

### PSO + Local Search

Apply a local search (gradient descent, Nelder-Mead, pattern search) to the global best periodically:
```
Every k iterations:
  g = local_search(g, budget=N_local_evals)
```

Combines PSO's global search with a local optimizer's precision.

---

## Constrained Optimization {#constrained}

### Penalty Functions

Add constraint violation to the objective:
```
F(x) = f(x) + lambda * sum_j max(0, g_j(x))^2
```

Lambda can be static, dynamic (increasing over time), or adaptive.

### Feasibility Rules (Deb's Rules)

When comparing two particles:
1. Feasible always beats infeasible
2. Between two feasible, better objective wins
3. Between two infeasible, lower total constraint violation wins

Simple, effective, and parameter-free. Widely used with PSO.

### Fly-Back Mechanism

When a particle violates constraints, reset to its previous feasible position:
```
if not feasible(x_i(t+1)):
  x_i(t+1) = x_i(t)  # or last known feasible position
```

### Epsilon-Constraint Method

Relax constraint boundaries over time:
```
epsilon(t) = epsilon_0 * (1 - t/t_max)^cp
```

Initially allows constraint violations, gradually tightening to enforce feasibility.

---

## Multimodal / Niching PSO {#multimodal}

For finding MULTIPLE optima simultaneously:

### Speciation PSO

1. Sort particles by fitness
2. Best unassigned particle becomes species seed
3. All particles within radius r_s of the seed join that species
4. Each species runs independent PSO with its own local best

### Fitness Sharing

Reduce fitness of particles in crowded regions:
```
f_shared(x_i) = f(x_i) / sum_j sh(d(x_i, x_j))
sh(d) = 1 - (d/sigma_share)^alpha if d < sigma_share, else 0
```

### Function Stretching

After locating an optimum, transform the landscape to repel particles:
```
H(x) = f(x) + gamma * sign(f(x) - f(x*)) * |f(x) - f(x*)|
```

Forces the swarm to abandon the found optimum and search for others.

### Ring Topology for Multimodal

The ring topology naturally supports multimodal search because information propagates slowly, allowing different sections of the ring to converge to different optima.
