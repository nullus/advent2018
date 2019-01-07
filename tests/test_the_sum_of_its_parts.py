# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.input import text
from advent.the_sum_of_its_parts import part1, part2

test_data = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def test_part1():
    assert "CABDFE" == part1(test_data)


def test_part2():
    assert 15 == part2(test_data, 2, 0)


def test_part1_with_puzzle_input():
    assert "GNJOCHKSWTFMXLYDZABIREPVUQ" == part1(text("the_sum_of_its_parts"))


def test_part2_with_puzzle_input():
    assert 886 == part2(text("the_sum_of_its_parts"))
