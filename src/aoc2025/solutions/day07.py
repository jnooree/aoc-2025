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
