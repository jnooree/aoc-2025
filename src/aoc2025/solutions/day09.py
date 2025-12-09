import numpy as np
from scipy.spatial import distance as D
from typer import FileText


def _area(p: np.ndarray, q: np.ndarray):
    return (np.abs(p[0] - q[0]) + 1) * (np.abs(p[1] - q[1]) + 1)


def main(data: FileText):
    pts = np.loadtxt(data, dtype=np.int64, delimiter=",")

    areas = D.pdist(pts, metric=_area)
    print(areas.max())
