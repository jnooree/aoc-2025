import numpy as np
import torch
from torch.nn import functional as F
from typer import FileText


def main(data: FileText):
    grid = (
        np.genfromtxt(
            data,
            dtype=np.str_,
            delimiter=1,
            deletechars=None,
            invalid_raise=True,
        )
        == "@"
    )
    grid = torch.from_numpy(grid).to(torch.int32)

    kernel = grid.new_ones(1, 1, 3, 3)
    kernel[..., 1, 1] = 0
    nbrs = F.conv2d(grid[None, None], kernel, padding="same").squeeze()

    print(torch.sum((nbrs < 4) & (grid == 1)).item())
