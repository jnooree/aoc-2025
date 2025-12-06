import numpy as np
from typer import FileText


def main(data: FileText):
    lines = data.read().splitlines()
    nums = np.loadtxt(lines[:-1], dtype=np.int64)
    ops = np.loadtxt([lines[-1]], dtype=np.str_)

    mul = np.prod(nums[:, ops == "*"], axis=0)
    add = np.sum(nums[:, ops == "+"], axis=0)
    print(np.sum(mul) + np.sum(add))
