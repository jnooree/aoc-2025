import numpy as np
from typer import FileText


def main(data: FileText):
    manifold = np.genfromtxt(data, dtype=np.str_, delimiter=1)

    beams = manifold[0] == "S"
    nsplit = 0
    for row in manifold[1:]:
        splitter = row == "^"
        nsplit += np.sum(splitter[beams])

        splitted = splitter & beams
        beams = (
            (beams & ~splitted)
            | np.insert(splitted[:-1], 0, False)
            | np.append(splitted[1:], False)
        )
    print(nsplit)

    prev_ntraj = (manifold[0] == "S").astype(np.int64)
    for row in manifold[1:]:
        splitter = row == "^"
        splitter_idxs = np.argwhere(splitter).flatten()
        if splitter_idxs.size == 0:
            continue

        next_ntraj = np.zeros_like(prev_ntraj)
        next_ntraj[~splitter] = prev_ntraj[~splitter]
        next_ntraj[splitter_idxs - 1] += prev_ntraj[splitter]
        next_ntraj[splitter_idxs + 1] += prev_ntraj[splitter]

        prev_ntraj = next_ntraj

    print(np.sum(prev_ntraj))
