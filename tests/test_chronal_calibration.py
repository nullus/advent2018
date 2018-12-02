# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark
from advent.chronal_calibration import part1, part2


test_part1_data = [
    ["+1 +1 +1", 3],
    ["+1 +1 -2", 0],
    ["-1 -2 -3", -6],
]


@mark.parametrize("adjustment, frequency", test_part1_data)
def test_part1(adjustment, frequency):
    assert part1(adjustment) == frequency


test_part2_data = [
    ["+1 -1", 0],
    ["+3 +3 +4 -2 -4", 10],
    ["-6 +3 +8 +5 -6", 5],
    ["+7 +7 -2 -7 -4", 14],
]


@mark.parametrize("adjustment, frequency", test_part2_data)
def test_part2(adjustment, frequency):
    assert part2(adjustment) == frequency
