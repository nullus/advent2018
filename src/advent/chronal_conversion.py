# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import Iterator


def _value_of_r3() -> Iterator[int]:
    """
    Translated from chronal_conversion
    """

    r1, r3 = 0, 0
    while True:
        r1 = r3 | 65536
        r3 = 9450265
        while r1 != 0:
            r3 = (((r3 + (r1 & 255)) & 16777215) * 65899) & 16777215
            r1 = int(r1 / 256)
        yield r3


def part1() -> int:
    return next(_value_of_r3())


def part2() -> int:
    seen_r3 = set()
    last_r3 = None
    for r3 in _value_of_r3():
        if r3 in seen_r3:
            break
        seen_r3.add(r3)
        last_r3 = r3

    return last_r3
