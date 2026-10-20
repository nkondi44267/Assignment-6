"""Reproducible comparison of median-of-medians vs randomized Quickselect.

Execute from repository root, e.g.:
    python -m src.benchmark --sizes 1000 5000 20000 50000 --repeats 7

Results are wall-clock runtimes from time.perf_counter_ns() in milliseconds;
CPU, Python runtime, OS scheduling, and machine load affect measured values.
"""

from __future__ import annotations

import argparse
import csv
import json
import platform
import random
import statistics
import time
from pathlib import Path

from .selection import deterministic_select, randomized_quickselect


def generate_input(distribution: str, n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    if distribution == "random":
        return [rng.randrange(-n * 10, n * 10 + 1) for _ in range(n)]
    if distribution == "sorted":
        return list(range(n))
    if distribution == "reverse":
        return list(range(n, 0, -1))
    if distribution == "many_duplicates":
        return [rng.randrange(10) for _ in range(n)]
    raise ValueError(distribution)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000, 20000, 50000])
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--seed", type=int, default=674)
    parser.add_argument("--output", type=Path, default=Path("results/benchmark.csv"))
    args = parser.parse_args()
    if args.repeats < 1 or any(s < 1 for s in args.sizes):
        parser.error("sizes and repeats must be positive")

    algorithms = {
        "Median of Medians": deterministic_select,
        "Randomized Quickselect": randomized_quickselect,
    }
    rows: list[dict[str, str | int | float]] = []
    distributions = ["random", "sorted", "reverse", "many_duplicates"]
    for size in args.sizes:
        for distribution in distributions:
            data = generate_input(distribution, size, args.seed + size)
            k = (size + 1) // 2  # median rank, one based
            expected = sorted(data)[k - 1]  # deliberately NOT inside timed region
            for label, selector in algorithms.items():
                # Warm-up and verify all methods before measurements.
                warm_rng = random.Random(args.seed)
                warm_value = (selector(data, k) if label == "Median of Medians"
                              else selector(data, k, warm_rng))
                assert warm_value == expected
                durations = []
                for r in range(args.repeats):
                    start = time.perf_counter_ns()
                    found = (selector(data, k) if label == "Median of Medians"
                             else selector(data, k, random.Random(args.seed + r)))
                    elapsed_ns = time.perf_counter_ns() - start
                    assert found == expected
                    durations.append(elapsed_ns / 1_000_000)
                row = {
                    "n": size,
                    "distribution": distribution,
                    "algorithm": label,
                    "repeats": args.repeats,
                    "median_ms": round(statistics.median(durations), 5),
                    "mean_ms": round(statistics.mean(durations), 5),
                    "min_ms": round(min(durations), 5),
                    "max_ms": round(max(durations), 5),
                }
                rows.append(row)
                print(f"n={size:>6} {distribution:<16} {label:<23} "
                      f"median {row['median_ms']:>9.3f} ms")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    details = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "seed": args.seed,
        "sizes": args.sizes,
        "repeats": args.repeats,
        "measure": "median (and mean, minimum, maximum) of wall-clock elapsed milliseconds",
        "selection_rank": "one-based floor((n+1)/2)",
        "note": "fixed array per size/distribution; different randomized seeds per trial; input copy included; sorting used only to verify outside timing",
    }
    (args.output.parent / "benchmark_environment.json").write_text(
        json.dumps(details, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Saved {len(rows)} benchmark rows in {args.output}")


if __name__ == "__main__":
    main()
