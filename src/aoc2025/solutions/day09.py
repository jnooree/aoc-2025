import itertools
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.spatial import distance as D
from typer import FileText


def _area(p: np.ndarray, q: np.ndarray):
    return (np.abs(p[0] - q[0]) + 1) * (np.abs(p[1] - q[1]) + 1)


def _minmax_pts(p: np.ndarray, q: np.ndarray):
    pq = np.stack([p, q])
    pmin = pq.min(axis=0)
    pmax = pq.max(axis=0)
    return pmin, pmax


def _ngreen(psum: np.ndarray, p: np.ndarray, q: np.ndarray):
    p = p - 1
    return (
        psum[tuple(q)] - (psum[p[0], q[1]] + psum[q[0], p[1]]) + psum[tuple(p)]
    )


def main(data: FileText, outdir: Path = Path.cwd()):
    outdir.mkdir(parents=True, exist_ok=True)

    pts = np.loadtxt(data, dtype=np.int64, delimiter=",")

    areas = D.pdist(pts, metric=_area)
    print(areas.max())

    xs, xi = np.unique(pts[:, 0], return_inverse=True)
    ys, yi = np.unique(pts[:, 1], return_inverse=True)
    n = np.arange(len(pts))
    compressed = np.stack([n[xi], n[yi]], axis=1)

    cmap = np.zeros((len(xs), len(ys)), dtype=np.int64)
    for p, q in itertools.pairwise(
        np.append(compressed, compressed[:1], axis=0)
    ):
        if p[0] == q[0]:
            continue

        xmin, xmax = min(p[0], q[0]), max(p[0], q[0])
        y = p[1]

        cmap[xmin, y] = 1
        cmap[xmin + 1 : xmax, y] = 3
        cmap[xmax, y] = 2

    img = Image.fromarray((cmap > 0).astype(np.uint8) * 255, mode="L")
    img.save(outdir / "day09-vertical.png")

    for row in cmap:
        (border,) = np.where(row > 0)
        flag = 0
        for b, e in itertools.pairwise(border):
            flag ^= row[b]
            if flag == 0:
                continue

            row[b + 1 : e] = 1

    img = Image.fromarray((cmap > 0).astype(np.uint8) * 255, mode="L")
    img.save(outdir / "day09-filled.png")

    psum = (cmap > 0).cumsum(axis=1).cumsum(axis=0)

    amax = 0
    for cp, cq in itertools.combinations(compressed, 2):
        cp, cq = _minmax_pts(cp, cq)
        carea = np.prod(cq - cp + 1)
        ngreen = _ngreen(psum, cp, cq)
        if carea != ngreen:
            continue

        dx = xs[cq[0]] - xs[cp[0]] + 1
        dy = ys[cq[1]] - ys[cp[1]] + 1
        amax = max(amax, dx * dy)
    print(amax)
