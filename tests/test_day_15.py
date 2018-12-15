# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.
from pytest import mark

from advent.day_15 import part1, Battle, Vector, part2
from advent.input import text

test_battle1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip()

test_battle1_outcome = 27730

test_battle1_map = """
#######
#.....#
#.....#
#.#.#.#
#...#.#
#.....#
#######
""".strip().splitlines()


def test_part1():
    assert test_battle1_outcome == part1(test_battle1)


def test_battle_map():
    assert test_battle1_map == Battle(test_battle1).map


def test_battle_actors():
    assert 6 == len(Battle(test_battle1).actors)


def test_battle_start_at_round_zero():
    assert 0 == Battle(test_battle1).round


def test_battle_str_matches_text():
    assert test_battle1 == str(Battle(test_battle1))


def test_battle_actors_health():
    assert 200 * 6 == sum(actor.hit_points for actor in Battle(test_battle1).actors.values())


test_data_battle1_space_is_empty = [
    [1, 1, True],
    [2, 3, False],
    [3, 4, False],
    [3, 6, False],
    [3, 3, True],
]


@mark.parametrize("x, y, is_empty", test_data_battle1_space_is_empty)
def test_battle_space_is_empty(x, y, is_empty):
    assert is_empty == Battle(test_battle1).is_empty(Vector(x, y))


def test_part1_with_puzzle_input():
    assert 245280 == part1(text('day_15'))


def test_part2_with_puzzle_input():
    assert 74984 == part2(text('day_15'))

