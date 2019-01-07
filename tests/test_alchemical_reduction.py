# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.alchemical_reduction import part1, part2
from advent.input import text


def test_part1():
    assert 10 == part1("dabAcCaCBAcCcaDA")


def test_part2():
    assert 4 == part2("dabAcCaCBAcCcaDA")


def test_part1_with_puzzle_input():
    assert 10250 == part1(text("alchemical_reduction"))


def test_part2_with_puzzle_input():
    assert 6188 == part2(text("alchemical_reduction"))
