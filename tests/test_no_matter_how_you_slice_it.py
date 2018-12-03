# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.no_matter_how_you_slice_it import part1, part2, parse_claims_text, Claim

test_data = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""


def test_claims():
    assert Claim("#1", 1, 3, 4, 4) == next(parse_claims_text("#1 @ 1,3: 4x4"))


def test_part1():
    assert 4 == part1(test_data)


def test_part2():
    assert "#3" == part2(test_data)
