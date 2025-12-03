import numpy as np
from typer import FileText


def main(data: FileText):
    nums = np.genfromtxt(data, dtype=np.int64, delimiter=1, invalid_raise=True)
    n = nums.shape[1]
    indices = np.arange(n)

    first = np.argmax(nums[:, :-1], axis=1, keepdims=True)
    masked_nums = np.where(indices > first, nums, -1)
    second = np.argmax(masked_nums, axis=1, keepdims=True)

    joltages = 10 * np.take_along_axis(
        nums, first, axis=1
    ) + np.take_along_axis(nums, second, axis=1)
    print(np.sum(joltages))

    total = 0
    masked_nums = nums
    for i in reversed(range(12)):
        argdigit = np.argmax(
            masked_nums[:, : -i or None],
            axis=1,
            keepdims=True,
        )
        total = total * 10 + np.take_along_axis(masked_nums, argdigit, axis=1)
        masked_nums = np.where(indices > argdigit, masked_nums, -1)

    print(np.sum(total))
