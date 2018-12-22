# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from functools import lru_cache
from operator import sub
from typing import Tuple


@lru_cache(maxsize=9000)
def erosion_level(coords: Tuple[int, int], depth: int) -> int:
    return (geologic_index(coords, depth) + depth) % 20183


@lru_cache(maxsize=9000)
def geologic_index(coords: Tuple[int, int], depth: int) -> int:
    if coords[0] == 0:
        return coords[1] * 48271
    elif coords[1] == 0:
        return coords[0] * 16807
    else:
        return (
            erosion_level(tuple(map(sub, coords, (1, 0))), depth) *
            erosion_level(tuple(map(sub, coords, (0, 1))), depth)
        )


def part1(coords: Tuple[int, int], depth: int) -> int:
    return sum(
        erosion_level((x, y), depth) % 3
        for y in range(0, coords[1] + 1)
        for x in range(0, coords[0] + 1)
        if (x, y) != coords
    )
