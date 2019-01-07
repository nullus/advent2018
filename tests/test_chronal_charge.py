# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.chronal_charge import power_level, part1, part2
from advent.input import text


def test_power_level():
    assert 4 == power_level(3, 5, 8)


test_power_level_data = [
    [[122, 79, 57], -5],
    [[217, 196, 39], 0],
    [[101, 153, 71], 4],
]


@mark.parametrize("params, level", test_power_level_data)
def test_power_levels(params, level):
    assert level == power_level(*params)


test_part1_data = [
    [18, (33, 45)],
    [42, (21, 61)],
]


@mark.parametrize("serial, coordinates", test_part1_data)
def test_part1(serial, coordinates):
    assert coordinates == part1(serial)


test_part2_data = [
    [18, (90, 269, 16)],
    [42, (232, 251, 12)],
]


@mark.slow
@mark.parametrize("serial, coordinates", test_part2_data)
def test_part2(serial, coordinates):
    assert coordinates == part2(serial)


def test_part1_with_puzzle_input():
    assert (235, 14) == part1(int(text("chronal_charge")))


@mark.slow
def test_part2_with_puzzle_input():
    assert (237, 227, 14) == part2(int(text("chronal_charge")))
