import numpy as np
from typer import FileText


def main(data: FileText):
    nums = np.genfromtxt(data, dtype=np.int8, delimiter=1, invalid_raise=True)
    n = nums.shape[1]

    first = np.argmax(nums[:, :-1], axis=1, keepdims=True)

    indices = np.arange(n)
    masked_nums = np.where(indices > first, nums, -1)
    second = np.argmax(masked_nums, axis=1, keepdims=True)

    joltages = 10 * np.take_along_axis(
        nums, first, axis=1
    ) + np.take_along_axis(nums, second, axis=1)
    print(np.sum(joltages))
