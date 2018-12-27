# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from textwrap import dedent

from pytest import mark

from advent.four_dimensional_adventure import part1, KdTree, Node, parse
from advent.input import text

test_data = [
    [dedent("""
        0,0,0,0
        3,0,0,0
        0,3,0,0
        0,0,3,0
        0,0,0,3
        0,0,0,6
        9,0,0,0
        12,0,0,0
    """).strip(), 2],
    [dedent("""
        -1,2,2,0
        0,0,2,-2
        0,0,0,-2
        -1,2,0,0
        -2,-2,-2,2
        3,0,2,-1
        -1,3,2,2
        -1,0,-1,0
        0,2,1,-2
        3,0,0,0
    """).strip(), 4],
    [dedent("""
        1,-1,0,1
        2,0,-1,0
        3,2,-1,0
        0,0,3,1
        0,0,-1,-1
        2,3,-2,0
        -2,2,0,0
        2,-2,0,-1
        1,-1,0,-1
        3,2,0,2
    """).strip(), 3],
    [dedent("""
        1,-1,-1,-2
        -2,-2,0,1
        0,2,1,3
        -2,3,-2,1
        0,2,3,-2
        -1,-1,1,-2
        0,-2,-1,0
        -2,2,3,-1
        1,2,2,0
        -1,-2,0,-2
    """).strip(), 8],
]


@mark.parametrize("puzzle_input, constellations", test_data)
def test_part1(puzzle_input, constellations):
    assert constellations == part1(puzzle_input)


def test_kdtree():
    points = ((3, 1), (2, 4), (2, 3), (1, 5))
    kdtree = KdTree(2, points)

    assert Node((2, 4), Node((1, 5), None, None), Node((2, 3), Node((3, 1), None, None), None)) == kdtree.root


def test_kdtree_points_in_range():
    points = ((3, 1), (2, 4), (2, 3), (1, 5))
    kdtree = KdTree(2, points)

    assert {(3, 1), (2, 3)} == set(kdtree.points_in_range((1, 1), 3))


def test_parse():
    assert [(-1, 2, -3, 20), (2, 50, -6, 9)] == list(parse(
        dedent("""
        -1,2,-3,20
        2,50,-6,9
        """).strip()
    ))


def test_part1_with_puzzle_input():
    assert 425 == part1(text("four_dimensional_adventure"))
