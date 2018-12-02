# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import cycle
from typing import Set


def part1(adjustments: str) -> int:
    return sum(int(i) for i in adjustments.split())


def part2(adjustments: str) -> int:
    frequencies: Set[int] = {0}
    value = 0
    for i in cycle(adjustments.split()):
        value += int(i)
        if value in frequencies:
            return value
        frequencies.add(value)
