"""
Standard Particle Swarm Optimization implementation.

Supports:
- Global best (gbest) and local best (lbest/ring) topologies
- Von Neumann topology
- Constriction factor or inertia weight (constant or linear decay)
- Velocity clamping and multiple boundary handling strategies
- Latin Hypercube initialization
- Convergence tracking and diversity monitoring
"""

import numpy as np
from typing import Callable, Optional, Tuple, List, Dict, Any


class PSOResult:
    """Container for PSO optimization results."""
    def __init__(self, best_position: np.ndarray, best_fitness: float,
                 history: List[float], n_evaluations: int,
                 diversity_history: List[float], final_positions: np.ndarray):
        self.best_position = best_position
        self.best_fitness = best_fitness
        self.history = history
        self.n_evaluations = n_evaluations
        self.diversity_history = diversity_history
        self.final_positions = final_positions

    def __repr__(self):
        return (f"PSOResult(best_fitness={self.best_fitness:.6e}, "
                f"n_evaluations={self.n_evaluations})")


class PSO:
    """
    Configurable Particle Swarm Optimizer.

    Parameters
    ----------
    objective_fn : callable
        Function to minimize. Takes a 1D numpy array, returns a scalar.
    bounds : list of tuples
        [(lb_1, ub_1), (lb_2, ub_2), ...] for each dimension.
    n_particles : int
        Swarm size. Default 40 (SPSO-2011 recommendation).
    topology : str
        'gbest' (global), 'ring' (local, k=2), 'von_neumann' (grid).
    w : float or str
        Inertia weight. Float for constant, 'linear_decay' for 0.9->0.4,
        'constriction' to use constriction factor.
    c1 : float
        Cognitive coefficient. Default 1.49618 (constriction-derived).
    c2 : float
        Social coefficient. Default 1.49618 (constriction-derived).
    max_iter : int
        Maximum iterations.
    max_eval : int or None
        Maximum function evaluations (overrides max_iter if set).
    v_max_fraction : float
        Velocity clamp as fraction of search range per dimension. Default 1.0.
    boundary_handling : str
        'absorb', 'reflect', 'random', or 'wrap'.
    init_method : str
        'random' or 'lhs' (Latin Hypercube Sampling).
    target_fitness : float or None
        Stop early if this fitness is achieved.
    stagnation_limit : int
        Stop if no improvement for this many iterations. 0 = disabled.
    seed : int or None
        Random seed for reproducibility.
    verbose : bool
        Print progress every 10% of iterations.
    """

    def __init__(
        self,
        objective_fn: Callable[[np.ndarray], float],
        bounds: List[Tuple[float, float]],
        n_particles: int = 40,
        topology: str = 'gbest',
        w: Any = 0.7298,
        c1: float = 1.49618,
        c2: float = 1.49618,
        max_iter: int = 1000,
        max_eval: Optional[int] = None,
        v_max_fraction: float = 1.0,
        boundary_handling: str = 'absorb',
        init_method: str = 'random',
        target_fitness: Optional[float] = None,
        stagnation_limit: int = 0,
        seed: Optional[int] = None,
        verbose: bool = False,
    ):
        self.objective_fn = objective_fn
        self.bounds = np.array(bounds, dtype=float)
        self.n_dims = len(bounds)
        self.n_particles = n_particles
        self.topology = topology
        self.w_config = w
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter
        self.max_eval = max_eval
        self.v_max_fraction = v_max_fraction
        self.boundary_handling = boundary_handling
        self.init_method = init_method
        self.target_fitness = target_fitness
        self.stagnation_limit = stagnation_limit
        self.verbose = verbose

        if seed is not None:
            np.random.seed(seed)

        self.lb = self.bounds[:, 0]
        self.ub = self.bounds[:, 1]
        self.range = self.ub - self.lb
        self.v_max = self.v_max_fraction * self.range

        # Constriction factor setup
        self.use_constriction = (w == 'constriction')
        if self.use_constriction:
            phi = c1 + c2
            if phi <= 4:
                raise ValueError(f"c1 + c2 must be > 4 for constriction (got {phi})")
            self.K = 2.0 / abs(2.0 - phi - np.sqrt(phi**2 - 4 * phi))

        # Von Neumann grid dimensions
        if topology == 'von_neumann':
            self._setup_von_neumann_grid()

    def _setup_von_neumann_grid(self):
        """Compute rows/cols for Von Neumann grid topology."""
        S = self.n_particles
        rows = int(np.sqrt(S))
        while S % rows != 0:
            rows -= 1
        cols = S // rows
        self.grid_rows = rows
        self.grid_cols = cols

    def _get_w(self, t: int) -> float:
        """Get inertia weight for iteration t."""
        if self.use_constriction:
            return 1.0  # Constriction handles it
        if isinstance(self.w_config, (int, float)):
            return float(self.w_config)
        if self.w_config == 'linear_decay':
            return 0.9 - (0.9 - 0.4) * t / self.max_iter
        raise ValueError(f"Unknown w config: {self.w_config}")

    def _get_neighborhood_best(self, i: int, pbest_pos: np.ndarray,
                                pbest_fit: np.ndarray) -> np.ndarray:
        """Get the best position in particle i's neighborhood."""
        if self.topology == 'gbest':
            return pbest_pos[np.argmin(pbest_fit)]

        elif self.topology == 'ring':
            S = self.n_particles
            neighbors = [(i - 1) % S, i, (i + 1) % S]
            best = min(neighbors, key=lambda j: pbest_fit[j])
            return pbest_pos[best]

        elif self.topology == 'von_neumann':
            row, col = divmod(i, self.grid_cols)
            neighbors = [
                i,  # self
                ((row - 1) % self.grid_rows) * self.grid_cols + col,  # up
                ((row + 1) % self.grid_rows) * self.grid_cols + col,  # down
                row * self.grid_cols + (col - 1) % self.grid_cols,    # left
                row * self.grid_cols + (col + 1) % self.grid_cols,    # right
            ]
            best = min(neighbors, key=lambda j: pbest_fit[j])
            return pbest_pos[best]

        raise ValueError(f"Unknown topology: {self.topology}")

    def _handle_boundaries(self, positions: np.ndarray,
                           velocities: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Handle particles that leave the search space."""
        if self.boundary_handling == 'absorb':
            below = positions < self.lb
            above = positions > self.ub
            positions = np.clip(positions, self.lb, self.ub)
            velocities[below | above] = 0

        elif self.boundary_handling == 'reflect':
            for d in range(self.n_dims):
                below = positions[:, d] < self.lb[d]
                above = positions[:, d] > self.ub[d]
                positions[below, d] = 2 * self.lb[d] - positions[below, d]
                positions[above, d] = 2 * self.ub[d] - positions[above, d]
                velocities[below, d] *= -1
                velocities[above, d] *= -1
            positions = np.clip(positions, self.lb, self.ub)

        elif self.boundary_handling == 'random':
            oob = (positions < self.lb) | (positions > self.ub)
            random_pos = self.lb + self.range * np.random.rand(*positions.shape)
            positions = np.where(oob, random_pos, positions)
            velocities[oob] = 0

        elif self.boundary_handling == 'wrap':
            for d in range(self.n_dims):
                positions[:, d] = self.lb[d] + (
                    positions[:, d] - self.lb[d]) % self.range[d]

        return positions, velocities

    def _compute_diversity(self, positions: np.ndarray) -> float:
        """Compute swarm diversity as mean standard deviation across dimensions."""
        return float(np.mean(np.std(positions, axis=0) / self.range))

    def optimize(self) -> PSOResult:
        """Run PSO optimization. Returns PSOResult."""
        # Initialize positions
        if self.init_method == 'lhs':
            try:
                from scipy.stats import qmc
                sampler = qmc.LatinHypercube(d=self.n_dims)
                sample = sampler.random(n=self.n_particles)
                positions = self.lb + self.range * sample
            except ImportError:
                positions = self.lb + self.range * np.random.rand(
                    self.n_particles, self.n_dims)
        else:
            positions = self.lb + self.range * np.random.rand(
                self.n_particles, self.n_dims)

        # Initialize velocities (zero or random)
        velocities = np.zeros((self.n_particles, self.n_dims))

        # Evaluate initial fitness
        fitness = np.array([self.objective_fn(p) for p in positions])
        n_eval = self.n_particles

        # Personal bests
        pbest_pos = positions.copy()
        pbest_fit = fitness.copy()

        # Global best
        gbest_idx = np.argmin(fitness)
        gbest_pos = positions[gbest_idx].copy()
        gbest_fit = fitness[gbest_idx]

        # Tracking
        history = [gbest_fit]
        diversity_history = [self._compute_diversity(positions)]
        stagnation_count = 0

        for t in range(self.max_iter):
            w = self._get_w(t)

            # Update each particle
            for i in range(self.n_particles):
                r1 = np.random.rand(self.n_dims)
                r2 = np.random.rand(self.n_dims)

                nbest = self._get_neighborhood_best(i, pbest_pos, pbest_fit)

                cognitive = self.c1 * r1 * (pbest_pos[i] - positions[i])
                social = self.c2 * r2 * (nbest - positions[i])

                if self.use_constriction:
                    velocities[i] = self.K * (
                        velocities[i] + cognitive + social)
                else:
                    velocities[i] = w * velocities[i] + cognitive + social

                # Velocity clamping
                velocities[i] = np.clip(velocities[i], -self.v_max, self.v_max)

                # Position update
                positions[i] = positions[i] + velocities[i]

            # Boundary handling
            positions, velocities = self._handle_boundaries(positions, velocities)

            # Evaluate fitness
            fitness = np.array([self.objective_fn(p) for p in positions])
            n_eval += self.n_particles

            # Update personal bests
            improved = fitness < pbest_fit
            pbest_pos[improved] = positions[improved]
            pbest_fit[improved] = fitness[improved]

            # Update global best
            best_idx = np.argmin(pbest_fit)
            if pbest_fit[best_idx] < gbest_fit:
                gbest_pos = pbest_pos[best_idx].copy()
                gbest_fit = pbest_fit[best_idx]
                stagnation_count = 0
            else:
                stagnation_count += 1

            # Track
            history.append(gbest_fit)
            diversity_history.append(self._compute_diversity(positions))

            # Verbose output
            if self.verbose and (t + 1) % max(1, self.max_iter // 10) == 0:
                div = diversity_history[-1]
                print(f"Iter {t+1}/{self.max_iter} | "
                      f"Best: {gbest_fit:.6e} | Diversity: {div:.4f}")

            # Stopping criteria
            if self.target_fitness is not None and gbest_fit <= self.target_fitness:
                break
            if self.max_eval and n_eval >= self.max_eval:
                break
            if self.stagnation_limit and stagnation_count >= self.stagnation_limit:
                break

        return PSOResult(
            best_position=gbest_pos,
            best_fitness=gbest_fit,
            history=history,
            n_evaluations=n_eval,
            diversity_history=diversity_history,
            final_positions=positions,
        )


# ----- Benchmark Functions -----

def sphere(x: np.ndarray) -> float:
    return float(np.sum(x**2))

def rosenbrock(x: np.ndarray) -> float:
    return float(np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2))

def rastrigin(x: np.ndarray) -> float:
    n = len(x)
    return float(10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x)))

def ackley(x: np.ndarray) -> float:
    n = len(x)
    s1 = np.sum(x**2)
    s2 = np.sum(np.cos(2 * np.pi * x))
    return float(-20 * np.exp(-0.2 * np.sqrt(s1 / n))
                 - np.exp(s2 / n) + 20 + np.e)

def griewank(x: np.ndarray) -> float:
    s = np.sum(x**2) / 4000
    p = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
    return float(s - p + 1)


if __name__ == '__main__':
    print("=== PSO Benchmark Tests ===\n")

    benchmarks = [
        ("Sphere (10D)", sphere, [(-100, 100)] * 10, 1e-10),
        ("Rastrigin (10D)", rastrigin, [(-5.12, 5.12)] * 10, 1.0),
        ("Rosenbrock (10D)", rosenbrock, [(-30, 30)] * 10, 10.0),
        ("Ackley (10D)", ackley, [(-32, 32)] * 10, 1.0),
    ]

    for name, fn, bounds, threshold in benchmarks:
        result = PSO(
            fn, bounds, n_particles=40, topology='gbest',
            w='linear_decay', max_iter=2000, seed=42
        ).optimize()
        status = "PASS" if result.best_fitness <= threshold else "FAIL"
        print(f"[{status}] {name}: {result.best_fitness:.6e} "
              f"({result.n_evaluations} evals)")

    print("\nDone.")
