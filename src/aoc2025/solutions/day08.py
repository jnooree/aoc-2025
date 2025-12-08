import numpy as np
from scipy.spatial import distance as D
from typer import FileText


def main(data: FileText, n: int = 1000):
    coords = np.loadtxt(data, dtype=np.int64, delimiter=",")

    N = len(coords)

    comp_ids = np.arange(N)
    comps: dict[int, set[int]] = {i: {i} for i in comp_ids}

    dmat = D.cdist(coords, coords, metric="sqeuclidean")
    inf = dmat.max() * 10
    dmat[np.tril_indices_from(dmat)] = inf

    idxs = np.stack(
        np.unravel_index(np.argsort(dmat.flatten()), dmat.shape),
        axis=1,
    )

    for i, j in idxs[:n]:
        ci = comp_ids[i]
        cj = comp_ids[j]
        if ci == cj:
            continue

        icomp = comps[ci]
        jcomp = comps[cj]
        cnew, merged, cold, old = (
            (cj, jcomp, ci, icomp)
            if len(icomp) < len(jcomp)
            else (ci, icomp, cj, jcomp)
        )
        merged |= old
        comp_ids[list(old)] = cnew
        del comps[cold]

    lens = np.partition(list(map(len, comps.values())), len(comps) - 3)
    print(np.prod(lens[-3:]))
