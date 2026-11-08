# KNIGHT: Exact Local Certificates and Limitations of Variable-Elimination Ordering

This repository contains the source code, numerical records, and reproducibility checks accompanying the research article *KNIGHT: Exact Local Certificates and Limitations of Variable-Elimination Ordering*.

The experiments concern **normalized Davis–Putnam elimination**: tautological, duplicate, and strictly subsumed clauses are removed after each step. The numerical objective in the connected-family theorem is the **sum of normalized clause counts after each hidden-variable elimination**, excluding the initial formula. It is not an estimate of SAT solver runtime.

## Repository contents

- `code/benchmark.py`: local certificate implementations, exact one-step oracle, synthetic CNF generators, and measured benchmark cohort.
- `code/coverage.py`: the reproducible 1,000-instance directed comparison, including exact and one-sided baselines.
- `code/semantic_checks.py`: checks of projected-function preservation and certificate soundness on finite cases.
- `code/connected_*.py`: independent full-CNF checks, exact state-space solvers, and constructive/depth-minimum certificates.
- `data/`: numerical results supporting the manuscript's tables and figures.
- `figures/plot_results.py`: regenerates the workflow, timing, and certificate-coverage graphics from the published tabular values.
- `docs/reproducibility.md`: commands, verification scope, and environment information.

## Reproduce the main checks

From the repository root, with Python 3.11 or later (standard library only for the tests):

```sh
python code/semantic_checks.py
python code/connected_full_cnf.py
python code/connected_symmetry_dp.py
python code/connected_schedules.py
python code/connected_unrestricted_depth.py
python code/connected_forced_depth.py
python code/benchmark.py --output /tmp/knight_benchmark_rerun.json
python code/coverage.py --output /tmp/knight_coverage_rerun.json
```

The exact dynamic program checks the finite copy counts listed in the accompanying results. The symbolic all-copy theorems are proved in the manuscript; computational checks are corroboration, **not** proof-assistant certification.

To regenerate the technical diagrams (requires Matplotlib):

```sh
python figures/plot_results.py
```

Recorded timing values are specific to the original experimental environment. Repeated runs can produce different timings, while the deterministic certificate outcomes and formula checks should agree.

## Availability and scope

The programs use synthetic CNFs; there are no confidential or third-party datasets. All files here directly support a result, figure, table, algorithm, or proof check in the manuscript. The repository is limited to review and reproduction material, rather than earlier exploratory work. No claim is made about solver-wide performance, industrial benchmarks, or machine-checked formal proofs.
