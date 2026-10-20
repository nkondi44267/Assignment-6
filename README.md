# Assignment 6 — Medians, Order Statistics, and Elementary Data Structures

This repository contains Python implementations and a measured performance comparison for the two parts of **Assignment 6: Medians and Order Statistics & Elementary Data Structures**.

## Contents

```text
src/selection.py        Median of Medians; randomized Quickselect
src/structures.py       Dynamic array, matrix, array stack, circular array queue, singly linked list
src/demo.py             Short reproducible usage examples
src/benchmark.py        Benchmark driver; verifies correctness and saves actual timings
tests/                  Unit tests, edge cases, duplicate-rich cases
results/benchmark.csv   Measured results for four input distributions
results/benchmark_environment.json  Runtime metadata
results/selection_benchmark.png     Chart derived from the CSV
results/create_plot.py             Optional chart recreation script
results/test_results.txt            Log of successful automated tests
report/Assignment_6_Analysis_Report.docx   Formal report
```

## Requirements

- **Python 3.10+** (standard library only for algorithms, tests, and benchmarks).
- Optional: `matplotlib` to reproduce charts; the report and PNG already include one.
- No external datasets, internet connection, or installations are necessary to run the code and tests.

## Run

Open a terminal in the repository root and execute:

```bash
python -m src.demo
python -m unittest discover -s tests -v
python -m src.benchmark --sizes 1000 5000 20000 50000 --repeats 7
```

The benchmark overwrites `results/benchmark.csv` and `results/benchmark_environment.json` with new local measurements; timings will vary across computers. To alter sizes, repetition count, or seed, use `--sizes`, `--repeats`, and `--seed`. No plotting package is required to run the benchmark.

## Selection API and examples

Both algorithms select the **k-th smallest** value with **1-based ranks** and leave the input unchanged.

```python
from src.selection import deterministic_select, randomized_quickselect
import random

values = [9, 1, 4, 4, 7]
assert deterministic_select(values, 3) == 4
assert randomized_quickselect(values, 3, random.Random(42)) == 4
assert values == [9, 1, 4, 4, 7]
```

### Complexity overview

| Operation / structure | Time | Auxiliary memory* |
|---|---|---|
| Median-of-Medians selection | Worst O(n) | O(n) including input copy and median lists |
| Randomized Quickselect | Expected O(n); worst O(n²) | O(n) including input copy |
| Dynamic array: indexed access / update | O(1) | O(n) storage |
| Dynamic array: append | Amortized O(1) | O(n) storage |
| Dynamic array: middle insert / delete | O(n) | O(n) storage |
| Matrix: indexed access / update | O(1) | O(rows × columns) storage |
| Matrix: insert/delete row | O(rows + columns) worst amortized | O(rows × columns) storage |
| Matrix: insert/delete column | O(rows × columns) | O(rows × columns) storage |
| Array stack: push / pop / peek | Amortized O(1) / amortized O(1) / O(1) | O(n) storage |
| Circular array queue: enqueue / dequeue / peek | Amortized O(1) / amortized O(1) / O(1) | O(n) storage |
| Singly linked list: prepend / append | O(1) | O(n) storage |
| Singly linked list: index access / search / delete by value | O(n) | O(n) storage |
| Singly linked list: insert at known head/tail | O(1) | O(n) storage |

*Auxiliary memory for selection includes the caller-safe input copy; storage for data structures is total retained space. Resizing individual push/pop operations can be O(n) even when amortized O(1).

## Benchmark interpretation

The report compares random, sorted, reverse-sorted, and duplicate-heavy inputs. The optional rooted-tree extension mentioned in the assignment was not implemented. For each test case, the driver performs a warm-up, checks correctness against a sorted reference **outside the timed region**, and reports median elapsed time from seven trials. Timings are not a controlled hardware benchmark and should not be generalized to every Python runtime or machine. Both procedures are compared on exactly the same input arrays and rank.

## GitHub submission steps

1. Create a **new empty repository** in your GitHub account (for example, `assignment-6-selection-and-data-structures`).
2. Copy all files from this project folder into that repository, preserving the directory structure.
3. From a terminal in this directory, run:

```bash
git init
git add .
git commit -m "Implement selection and elementary data structures with benchmarks"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Replace the URL with your real GitHub repository URL. **Submit the actual GitHub repository link in your course portal.** This deliverable is GitHub-ready; no repository was automatically created or published by the assistant.
