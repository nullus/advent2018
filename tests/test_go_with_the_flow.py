# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.go_with_the_flow import part1, part2
from advent.input import text

test_program = r'''
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
'''


def test_part1():
    assert 6 == part1(test_program)


@mark.slow
def test_part1_with_puzzle_input():
    assert 1694 == part1(text("go_with_the_flow_program"))


def test_part2_with_puzzle_input():
    assert 18964204 == part2(text("go_with_the_flow_program"))
