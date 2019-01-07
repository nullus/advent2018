# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.input import text
from advent.settlers_of_the_north_pole import parse, resource_value, next_state, part1, part2

test_area_initial_str = r'''
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
'''.strip()

test_area_step1_str = r'''
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.
'''.strip()

test_area_step10_str = r'''
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
'''.strip()


def test_parse_map():
    # Sample some regions in the test area

    map_ = parse(test_area_initial_str)

    assert '.' == map_[0][0]
    assert '#' == map_[2][8]
    assert '|' == map_[8][0]


def test_resource_value():
    assert 1147 == resource_value(parse(test_area_step10_str))


def test_next_state():
    assert parse(test_area_step1_str) == next_state(parse(test_area_initial_str))


def test_part1():
    assert 1147 == part1(test_area_initial_str)


def test_part1_with_puzzle_input():
    assert 355918 == part1(text("settlers_of_the_north_pole"))


@mark.slow
def test_part2_with_puzzle_input():
    assert 202806 == part2(text("settlers_of_the_north_pole"), 1_000_000_000)
