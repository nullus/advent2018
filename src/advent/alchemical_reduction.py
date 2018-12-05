# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import Optional, Callable, TypeVar

T = TypeVar('T')


def part1(polymer_input: str, filter_function: Optional[Callable[[T], T]] = None) -> int:
    polymer = list(filter(filter_function, polymer_input))

    i, length = 0, len(polymer)
    while i < length - 1:
        if polymer[i].swapcase() == polymer[i+1]:
            del polymer[i:i+2]
            length -= 2
            if i > 0:
                i -= 1
        else:
            i += 1

    return length


def part2(polymer_input: str) -> int:
    return min(
        part1(polymer_input, lambda x: x.lower() != i)
        for i in set(polymer_input.lower())
    )
