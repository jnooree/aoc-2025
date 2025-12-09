import numpy as np
from typer import FileText


def main(data: FileText):
    lines = data.read().splitlines()
    blank = lines.index("")

    ranges = np.loadtxt(lines[:blank], dtype=np.int64, delimiter="-")
    ids = np.array(lines[blank + 1 :], dtype=np.int64)

    fresh = np.any(
        (ids[:, None] >= ranges[:, 0]) & (ids[:, None] <= ranges[:, 1]),
        axis=-1,
    )
    print(np.sum(fresh))

    ranges[:, 1] += 1
    idxs = np.lexsort(np.flip(ranges.T, axis=0))
    ranges = ranges[idxs]

    merged = []
    current = range(*ranges[0])
    for r in ranges[1:]:
        if r[0] > current.stop:
            merged.append(current)
            current = range(*r)
            continue

        if r[1] > current.stop:
            current = range(current.start, r[1])
            continue
    merged.append(current)

    print(sum(map(len, merged)))
