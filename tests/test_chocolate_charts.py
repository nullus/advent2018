# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.chocolate_charts import part1, part2


test_data_initial_state = [3, 7]

test_data = [
    [9, "5158916779"],
    [5, "0124515891"],
    [18, "9251071085"],
    [2018, "5941429882"],
]


@mark.parametrize("recipes, next_scores", test_data)
def test_part1(recipes, next_scores):
    assert next_scores == part1(test_data_initial_state, recipes)


test_part2_data = [
    [9, "51589"],
    [5, "01245"],
    [18, "92510"],
    [2018, "59414"],
]


@mark.parametrize("recipes, sequence", test_part2_data)
def test_part2(recipes, sequence):
    assert recipes == part2(test_data_initial_state, sequence)

