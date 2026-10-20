"""Selection algorithms: deterministic median-of-medians and randomized Quickselect.

Both public functions accept any finite Sequence of comparable values and a
**one-based** rank k (k=1 selects the minimum; k=len(data) the maximum).
Neither function changes the caller's sequence. The algorithms use three-way
partitioning so duplicate values are handled correctly and efficiently.
"""

from __future__ import annotations

import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def _validate(data: Sequence[T], k: int) -> list[T]:
    """Copy data and reject invalid rank requests."""
    values = list(data)
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer rank (1-based)")
    if not 1 <= k <= len(values):
        raise ValueError(f"k must be between 1 and {len(values)}")
    return values


def _partition3(a: list[T], lo: int, hi: int, pivot: T) -> tuple[int, int]:
    """In-place Dutch-flag partition into <, ==, > pivot in a[lo:hi+1].

    Return the inclusive indices bounding the == pivot portion.
    """
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _median_of_medians(a: list[T], lo: int, hi: int) -> T:
    """Choose a worst-case-safe pivot from groups of at most five elements.

    Form the median from each group, then recursively select the median of
    these medians. A group-sort is constant-size (<= 5) work.
    """
    medians: list[T] = []
    for start in range(lo, hi + 1, 5):
        group = sorted(a[start:min(start + 5, hi + 1)])
        medians.append(group[len(group) // 2])
    if len(medians) == 1:
        return medians[0]
    return _select_in_place(medians, 0, len(medians) - 1, len(medians) // 2)


def _select_in_place(a: list[T], lo: int, hi: int, target: int) -> T:
    """Select zero-based target index within inclusive [lo, hi]."""
    while lo < hi:
        pivot = _median_of_medians(a, lo, hi)
        left_end, right_start = _partition3(a, lo, hi, pivot)
        if target < left_end:
            hi = left_end - 1
        elif target > right_start:
            lo = right_start + 1
        else:
            return a[target]
    return a[lo]


def deterministic_select(data: Sequence[T], k: int) -> T:
    """Return k-th smallest element with O(n) worst-case time.

    Works for duplicates and negative numbers. The copy and temporary median
    lists result in O(n) extra space; internal recursion is logarithmic deep.
    """
    a = _validate(data, k)
    return _select_in_place(a, 0, len(a) - 1, k - 1)


def randomized_quickselect(
    data: Sequence[T], k: int, rng: random.Random | None = None
) -> T:
    """Return k-th smallest with expected O(n) time using a random pivot.

    Worst-case time is O(n^2), but uniform independent pivot selection yields
    O(n) *expected* time. The iterative implementation needs O(1) auxiliary
    space beyond the O(n) input copy; rng may be seeded for repeatable tests.
    """
    a = _validate(data, k)
    generator = rng if rng is not None else random.Random()
    lo, hi, target = 0, len(a) - 1, k - 1
    while lo < hi:
        pivot = a[generator.randint(lo, hi)]
        lt, gt = _partition3(a, lo, hi, pivot)
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return a[target]
    return a[lo]
