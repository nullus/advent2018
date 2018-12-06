# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.chronal_coordinates import part1, part2

test_day_7_data = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""


def test_part1():
    assert 17 == part1(test_day_7_data)


def test_part2():
    assert 16 == part2(test_day_7_data, 32)
