# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.mode_maze import erosion_level, geologic_index, part1, part2

test_geologic_index_data = [
    [(0, 0), 0],
    [(1, 0), 16807],
    [(1, 1), 145722555],
    [(0, 10), 482710]
]


@mark.parametrize("coords, index", test_geologic_index_data)
def test_geologic_index(coords, index):
    assert index == geologic_index(coords, 510)


test_erosion_level_data = [
    [(0, 0), 510, 510],
    [(1, 0), 510, 17317],
    [(0, 1), 510, 8415],
    [(1, 1), 510, 1805]
]


@mark.parametrize("coords, depth, level", test_erosion_level_data)
def test_erosion_level(coords, depth, level):
    assert level == erosion_level(coords, depth)


def test_part1():
    assert 114 == part1((10, 10), 510)


def test_part2():
    assert 45 == part2((10, 10), 510)


def test_part1_with_puzzle_input():
    assert 6_318 == part1((7, 782), 11_820)


@mark.slow
def test_part2_with_puzzle_input():
    assert 1_075 == part2((7, 782), 11_820)
