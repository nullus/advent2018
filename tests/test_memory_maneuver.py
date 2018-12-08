# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.memory_maneuver import part1, part2
from advent.input import text

test_data = """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
"""


def test_part1():
    assert 138 == part1(test_data)


def test_part1_with_puzzle_input():
    assert 35911 == part1(text('memory_maneuver'))


def test_part2():
    assert 66 == part2(test_data)


def test_part2_with_puzzle_input():
    assert 17206 == part2(text('memory_maneuver'))
