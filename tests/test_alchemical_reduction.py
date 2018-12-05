# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from advent.alchemical_reduction import part1, part2


def test_part1():
    assert 10 == part1("dabAcCaCBAcCcaDA")


def test_part2():
    assert 4 == part2("dabAcCaCBAcCcaDA")
