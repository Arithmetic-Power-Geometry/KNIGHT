# Recorded data

`manuscript_tables.json` contains the numeric values used in the five tables and the timing and coverage figures in the manuscript.

The four `.json.gz` files preserve original machine-readable records from the accompanying computational archive without altering their historical keys, names, or experimental values. They are gzip-compressed JSON, not Python pickles.

| File | Uncompressed SHA-256 |
| --- | --- |
| `original_benchmark_results.json.gz` | `ef05de3fbd4181ee24ee053b1204bc34c8d8238e810c7d514081d01956d30757` |
| `original_coverage_results.json.gz` | `5004e1bb0b3a2dd4046edbac0d6f1a9425b1d62174ae5eede0ce1bb7259797f1` |
| `original_local_audit_results.json.gz` | `452993d0536e7b981f5e141b1cb3c5339a789ec75e2bcbbc512a64bcb507c8b8` |
| `original_theorem_audit_results.json.gz` | `fd306c2f8a9a51e5995899b08fdde7acd6c2eac7971936165c2f02f4d0543aa0` |

To extract a record:

```sh
gzip -dc data/original_benchmark_results.json.gz > /tmp/knight_original_benchmark.json
```

The original timings and traced allocations are historical measurements. Fresh runs on other machines may differ. The code and deterministic random seeds permit independent replication of the underlying experimental comparisons; the raw files preserve the reported outputs.

The remaining uncompressed JSON files contain exact mathematical certificates and finite-state verification results. These calculations are checks of the manuscript's arguments, not formal proof-assistant verification.
