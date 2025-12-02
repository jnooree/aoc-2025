from pathlib import Path

import numpy as np


def main(data: Path):
    dis = np.loadtxt(
        data,
        dtype=np.int64,
        converters=lambda s: s.replace("R", "+").replace("L", "-"),
    )
    dis = np.insert(dis, 0, 50)
    pos = dis.cumsum()
    den, rem = np.divmod(pos, 100)

    print(np.sum(rem == 0))

    nrev = np.abs(den[1:] - den[:-1])

    left = dis < 0
    zero = rem == 0
    double = zero[:-1] & left[1:]
    missed = zero & left

    print(np.sum(nrev) - np.sum(double) + np.sum(missed))
