# Reproducibility

## Numerical definition

After each Davis–Putnam pivot, remove tautologies, exact duplicates and subsumed clauses. The size of a state is its resulting number of clauses. The global optimization objective sums these post-step sizes; it does not include the input CNF.

## Requirements

Python 3.11+ is sufficient for every script in `code/`. Matplotlib is required only for the graphs in `figures/`. No external datasets, SAT solver, or network access are needed.

## Local certificates and experimental tables

Run from the repository root:

```sh
python code/semantic_checks.py
python code/benchmark.py --output /tmp/benchmark_results.json
python code/coverage.py
```

The benchmark runs 27 cases: four all-tautological instances, three ordering-separation instances, and twenty seeded synthetic random CNFs. Each method is timed seven times; a separate `tracemalloc` pass records peak traced Python allocations. The coverage experiment tests 1,000 separately seeded random CNFs and compares both certificate methods, an exact-one-side test, and full exact lookahead.

`data/manuscript_tables.json` records the original values plotted and printed in the paper. Runtime measurements can vary across machines. Deterministic comparisons should reproduce the same certificate outcomes.

## Connected-family exact and symbolic certificates

```sh
python code/connected_full_cnf.py
python code/connected_unit_switch.py
python code/connected_symmetry_dp.py
python code/connected_schedules.py
python code/connected_unrestricted_depth.py
python code/connected_forced_depth.py
```

The independent full-CNF oracle checks all 16, 256, and 4,096 local-mask tuples for copy counts 1–3. The exact symmetry-reduced solver checks the first eight copy counts. Constructive schedules and both depth-wise optimization formulas have their own scripts. The recorded results reside in `data/`.

Finite verification checks the formulas over the scripted ranges. The theorem for arbitrary positive integer copy count is established through the mathematical argument in the paper, not by extrapolating finite test results.

## Figures

```sh
python -m pip install matplotlib
python figures/plot_results.py
```

The generated technical plots correspond to the paper's workflow and timing/coverage figures. The introductory chessboard image is conceptual and is not an experimental result.

## Notes on methods

The certificate returns a conclusion only for strict one-step normalized clause-count inequality; abstaining is inconclusive. The random inputs are synthetic. Memory numbers are traced Python allocations rather than operating-system resident memory. The repository does not claim formal proof-assistant certification or validation against production SAT solvers.
