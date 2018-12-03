# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.no_matter_how_you_slice_it import part1, claims, Claim, Rect, QTree, QNode

test_part1_data = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""


def test_claims():
    assert Claim("#1", 1, 3, 4, 4) == next(claims("#1 @ 1,3: 4x4"))


def test_empty_qtree():
    assert Rect(0, 0, 1000, 1000) == next(i for i in QTree(1000, 1000))


def test_qnode_split():
    qnode = QNode(Rect(0, 0, 1000, 1000))
    qnode.split(500, 500)
    assert Rect(0, 0, 500, 500) == qnode.child[0].bounds
    assert Rect(500, 0, 1000, 500) == qnode.child[1].bounds
    assert Rect(500, 500, 1000, 1000) == qnode.child[2].bounds
    assert Rect(0, 500, 500, 1000) == qnode.child[3].bounds


@mark.skip
def test_qtree_insert():
    qtree = QTree(1000, 1000)
    qtree.insert(Rect(333, 333, 666, 666))
    assert 7 == len(list(iter(qtree)))


@mark.skip
def test_part1():
    assert 4 == part1(test_part1_data)
