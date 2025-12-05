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
