# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.input import text
from advent.subterranean_sustainability import answer

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
    assert 325 == answer(test_data, 20)


def test_part1_with_puzzle_data():
    assert 2140 == answer(text('subterranean_sustainability'), 20)


def test_part2_with_puzzle_data():
    assert 1900000000384 == answer(text('subterranean_sustainability'), 50_000_000_000)
