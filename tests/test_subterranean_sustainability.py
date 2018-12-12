# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.input import text
from advent.subterranean_sustainability import part1, part2

test_data = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip()


def test_part1():
    assert 325 == part1(test_data)


def test_part1_with_puzzle_data():
    assert 2140 == part1(text('subterranean_sustainability'))


def test_part2_with_puzzle_data():
    assert 1900000000384 == part2(text('subterranean_sustainability'))
