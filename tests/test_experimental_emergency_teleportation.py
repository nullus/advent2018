# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.
from pytest import mark

from advent.experimental_emergency_teleportation import part1, part2, Cube

test_data = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".strip()


def test_part1():
    assert 7 == part1(test_data)


test_part2_data = """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""".strip()


def test_part2():
    assert 36 == part2(test_part2_data)


def test_cube_from_pos_and_r():
    assert (0, 0, 0) == Cube.from_pos_and_r((5, 5, 5), 5).min
    assert (10, 10, 10) == Cube.from_pos_and_r((5, 5, 5), 5).max


test_cube_intersection_data = [
    [Cube((0, 0, 0), (5, 5, 5)), Cube((4, 4, 4), (8, 8, 8)), Cube((4, 4, 4), (5, 5, 5))],
    [Cube((0, 5, 0), (5, 10, 5)), Cube((4, 0, 4), (8, 6, 8)), Cube((4, 5, 4), (5, 6, 5))],
]


@mark.parametrize("a, b, intersection", test_cube_intersection_data)
def test_cube_intersection(a, b, intersection):
    assert intersection == a.intersection(b)


def test_cube_valid():
    assert Cube((0, 0, 0), (10, 10, 10)).valid()


def test_cube_invalid():
    assert not Cube((0, 10, 0), (10, 0, 10)).valid()
