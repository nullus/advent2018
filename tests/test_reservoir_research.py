# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.input import text
from advent.reservoir_research import generate_map, part1, part2

test_data = r'''
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
'''.strip()

# This might be assumed
# test_spring_location = (500, 0)

test_map_output = r'''
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
'''.strip().splitlines()

test_map_output_array = [
    [tile for tile in row]
    for row in test_map_output
]


def test_map():
    assert ((494, 1), test_map_output_array) == generate_map(test_data)


def test_part1():
    assert 57 == part1(test_data)


def test_part1_with_puzzle_input():
    assert 32552 == part1(text('reservoir_research'))


def test_part2():
    assert 29 == part2(test_data)


def test_part2_with_puzzle_input():
    assert 26405 == part2(text('reservoir_research'))
