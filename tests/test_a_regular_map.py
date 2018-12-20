# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.a_regular_map import part1, part2
from advent.input import text

test_data = [
    ["^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23],
    ["^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31],
]


@mark.parametrize("map_regex, furthest_room", test_data)
def test_part1(map_regex, furthest_room):
    assert furthest_room == part1(map_regex)


def test_part1_with_puzzle_input():
    assert 3633 == part1(text("a_regular_map"))


def test_part2_with_puzzle_input():
    assert 8756 == part2(text("a_regular_map"))
