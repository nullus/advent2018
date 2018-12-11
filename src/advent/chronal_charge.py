# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from functools import lru_cache
from typing import Tuple


# Memoize the entire grid
@lru_cache(90_000)
def power_level(x: int, y: int, serial: int) -> int:
    return int(((x + 10) * y + serial) * (x + 10) / 100 % 10) - 5


@lru_cache(300)
def grid_power_levels(x: int, y: int, serial: int, size: int = 3) -> int:
    if size > 3:
        n = size - 1
        return grid_power_levels(x, y, serial, n) + sum(
            power_level(x + i, y + n, serial) + power_level(x + n, y + i, serial)
            for i in range(0, n)
        ) + power_level(x + n, y + n, serial)
    else:
        return sum(
            power_level(u, v, serial)
            for u in range(x, x + 3)
            for v in range(y, y + 3)
        )


def part1(serial: int) -> Tuple[int, int]:
    return max(
        ((grid_power_levels(x, y, serial), (x, y))
         for y in range(1, 298)
         for x in range(1, 298)),
        key=lambda k: k[0]
    )[1]


def part2(serial: int) -> Tuple[int, int, int]:
    return max(
        ((grid_power_levels(x, y, serial, z), (x, y, z))
         for y in range(1, 300)
         for x in range(1, 300)
         for z in range(3, 300)
         if y + z < 300 and x + z < 300
         ),
        key=lambda k: k[0]
    )[1]
