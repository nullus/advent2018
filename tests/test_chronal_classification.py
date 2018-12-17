# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.chronal_classification import part1, part2
from advent.input import text

test_data = r'''
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
'''.strip()


test_part2_output = None


def test_part1():
    assert 1 == part1(test_data)


def test_part2_with_puzzle_input():
    assert 594 == part2(text('chronal_classification'), text('chronal_classification_program'))
