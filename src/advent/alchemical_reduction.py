# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import List


def _react_list(polymer_list: List[str]) -> List[str]:
    # Don't mutate argument
    result = polymer_list.copy()

    i = 0
    while i < len(result) - 1:
        if result[i].swapcase() == result[i + 1]:
            del result[i:i + 2]
            if i > 0:
                i -= 1
        else:
            i += 1

    return result


def part1(polymer_input: str) -> int:
    return len(_react_list(list(polymer_input)))


def part2(polymer_input: str) -> int:
    polymer_base = _react_list(list(polymer_input))

    return min(
        len(_react_list([j for j in polymer_base if j.lower() != i]))
        for i in set(polymer_input.lower())
    )
