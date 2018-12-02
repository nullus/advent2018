# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark
from advent.inventory_management_system import is_letter_repeated_2_3_times, part1, part2, common_characters


test_is_letter_repeated_2_3_times_data = [
    ["abcdef", (0, 0)],
    ["bababc", (1, 1)],
    ["abbcde", (1, 0)],
    ["abcccd", (0, 1)],
    ["aabcdd", (1, 0)],
    ["abcdee", (1, 0)],
    ["ababab", (0, 1)],
]


@mark.parametrize("box_id, count", test_is_letter_repeated_2_3_times_data)
def test_is_letter_repeated_2_3_times(box_id, count):
    assert count == is_letter_repeated_2_3_times(box_id)


test_part1_data = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""


def test_part1():
    assert part1(test_part1_data) == 12


test_part2_data = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""


def test_part2():
    assert "fgij" == part2(test_part2_data)


test_common_characters_data = [
    ["fguij", "fghij", "fgij"],
    ["abcde", "pqrst", ""],
    ["abcde", "axcye", "ace"],
]


@mark.parametrize("this, that, common", test_common_characters_data)
def test_common_characters(this, that, common):
    assert common == common_characters(this, that)
