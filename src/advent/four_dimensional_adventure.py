# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import namedtuple
from operator import sub
from typing import Tuple, List, Optional, Iterable

Node = namedtuple('Node', ['point', 'left_child', 'right_child'])


class KdTree(object):
    def __init__(self, dimension, points: Iterable[Tuple[int, ...]]) -> None:
        super().__init__()
        self.dimension = dimension
        self.root: Optional[Node] = self.build_tree(list(points))

    def build_tree(self, points: List[Tuple[int, ...]], depth: int = 0) -> Optional[Node]:
        if not points:
            return None
        axis: int = depth % self.dimension
        points.sort(key=lambda k: k[axis])
        # TODO: Search for next
        split_index = [points[i][axis] for i in range(len(points) // 2 + 1)].index(points[len(points) // 2][axis])
        return Node(
            points[split_index],
            self.build_tree(points[:split_index], depth + 1),
            self.build_tree(points[split_index + 1:], depth + 1)
        )

    def points_in_range(self, point: Tuple[int, ...], distance: int) -> List[Tuple[int, ...]]:
        def _search_points_in_range(node: Node, depth: int) -> List[Tuple[int, ...]]:
            points = []
            if node is None:
                return points
            difference = tuple(map(sub, point, node.point))
            if sum(map(abs, difference)) <= distance:
                points.append(node.point)
            axis = depth % self.dimension
            if difference[axis] - distance < 0:
                points += _search_points_in_range(node.left_child, depth + 1)
            if difference[axis] + distance >= 0:
                points += _search_points_in_range(node.right_child, depth + 1)
            return points

        return _search_points_in_range(self.root, 0)


def parse(puzzle_input: str) -> Iterable[Tuple[int, ...]]:
    for line in puzzle_input.splitlines():
        yield tuple(map(int, line.split(",")))


def part1(puzzle_input: str) -> int:
    coordinates = list(parse(puzzle_input))

    kdtree = KdTree(4, coordinates)
    search = set(coordinates)
    constellations: int = 0
    while search:
        points = [search.pop()]
        while points:
            in_range = set(kdtree.points_in_range(points.pop(), 3))
            points.extend(search.intersection(in_range))
            search.difference_update(in_range)
        constellations += 1

    return constellations
