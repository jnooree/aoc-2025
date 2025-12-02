import itertools

import numpy as np
from typer import FileText


def _repeat_segment(seg: int, n: int = 2):
    return int(str(seg) * n)


def _extract_segment(num: int, s: int, n: int = 2):
    snum = str(num)
    l = len(snum)
    if l == s * n:
        return int(snum[:s])
    return 0


def _handle_segment(r: range, s: int, n: int = 2):
    segment = max(10 ** (s - 1), _extract_segment(r.start, s, n=n))
    nums = []
    while (
        len(str(segment)) == s
        and (num := _repeat_segment(segment, n=n)) < r.stop
    ):
        if num >= r.start:
            nums.append(num)
        segment += 1
    return nums


def _pt1_handle_range(r: range):
    lengths = np.arange(len(str(r.start)), len(str(r.stop)) + 1)
    segments = lengths[lengths % 2 == 0] // 2

    nums = list(
        itertools.chain.from_iterable(_handle_segment(r, s) for s in segments)
    )
    return nums


def _factorize(n: int):
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
            continue

        n //= i
        factors.append(i)

    if n > 1:
        factors.append(n)

    return factors


def _pt2_handle_range(r: range):
    lengths = np.arange(len(str(r.start)), len(str(r.stop)) + 1)
    factors = np.unique(
        list(itertools.chain.from_iterable(_factorize(l) for l in lengths))
    )

    all_nums = []
    for n in factors:
        segments = lengths[lengths % n == 0] // n
        all_nums.extend(
            itertools.chain.from_iterable(
                _handle_segment(r, s, n=n) for s in segments
            )
        )
    return np.unique(all_nums)


def main(data: FileText):
    ranges = [tuple(map(int, r.split("-"))) for r in data.read().split(",")]
    ranges = [range(b, e + 1) for b, e in ranges]

    all_nums = [_pt1_handle_range(r) for r in ranges]
    print(sum(itertools.chain.from_iterable(all_nums)))

    all_nums = [_pt2_handle_range(r) for r in ranges]
    print(sum(itertools.chain.from_iterable(all_nums)))
