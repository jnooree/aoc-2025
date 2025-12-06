import numpy as np
from typer import FileText


def main(data: FileText):
    lines = data.read().splitlines()
    nums = np.loadtxt(lines[:-1], dtype=np.int64)
    ops = np.loadtxt([lines[-1]], dtype=np.str_)

    mul = np.prod(nums[:, ops == "*"], axis=0)
    add = np.sum(nums[:, ops == "+"], axis=0)
    print(np.sum(mul) + np.sum(add))

    digits = np.array(list(map(list, lines[:-1])), dtype=np.str_).T

    (num_end,) = np.where(np.all(digits == " ", axis=1))
    num_end = np.append(num_end, digits.shape[0])
    num_begin = np.insert(num_end[:-1] + 1, 0, 0)

    nums = np.array(
        ["".join(line) if np.any(line != " ") else -1 for line in digits],
        dtype=np.int64,
    )

    total = 0
    for b, e, o in zip(num_begin, num_end, ops):
        oper = np.prod if o == "*" else np.sum
        total += oper(nums[b:e])
    print(total)
