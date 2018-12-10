# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.marble_mania import part1, part2

test_data = [
    [[9, 25], 32],
    [[13, 7999], 146373],
    [[10, 1618], 8317],
    [[17, 1104], 2764],
    [[21, 6111], 54718],
    [[30, 5807], 37305],
]


@mark.parametrize("args, score", test_data)
def test_part1(args, score):
    assert score == part1(*args)


@mark.parametrize("args, score", test_data)
def test_part2(args, score):
    assert score == part2(*args)
