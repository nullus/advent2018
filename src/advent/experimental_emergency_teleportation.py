# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.
from itertools import permutations, product
from operator import lt, le, sub, add
from pprint import pprint
from random import randrange
from re import match
from typing import Tuple, List


def _parse_coordinate_text(coordinate_text):
    nanobots = []
    for line in coordinate_text.splitlines():
        match_group = match(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$', line)
        if match_group:
            pos = tuple([int(match_group[1]), int(match_group[2]), int(match_group[3])])
            r = int(match_group[4])
            nanobots.append((pos, r))
    return nanobots


def part1(coordinate_text: str) -> int:
    nanobots = _parse_coordinate_text(coordinate_text)

    nanobots.sort(key=lambda k: k[1])

    count: int = 1
    for i in nanobots[:-1]:
        if sum(map(lambda a, b: abs(a - b), i[0], nanobots[-1][0])) <= nanobots[-1][1]:
            count += 1

    return count


class Cube(object):

    def __init__(self, min_: Tuple[int, int, int], max_: Tuple[int, int, int]) -> None:
        super().__init__()
        self.min = min_
        self.max = max_

    @classmethod
    def from_pos_and_r(cls, pos: Tuple[int, int, int], r: int):
        return Cube(tuple(map(lambda x: x - r, pos)), tuple(map(lambda x: x + r, pos)))

    def intersection(self, other):
        return Cube(tuple(map(max, self.min, other.min)), tuple(map(min, self.max, other.max)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cube):
            return False
        return self.min == other.min and self.max == other.max

    def __repr__(self) -> str:
        return f"Cube({self.min}, {self.max})"

    def valid(self) -> bool:
        return all(map(le, self.min, self.max))


def old_part2(coordinate_text: str) -> int:
    nanobots = _parse_coordinate_text(coordinate_text)

    # nanobots_bounds = [Cube.from_pos_and_r(nanobot[0], int(nanobot[1] / 2)) for nanobot in nanobots]
    #
    # # TODO: Can we do better than O(n^2)?
    # overlap = []
    # for i in nanobots_bounds:
    #     bounds: Cube = i
    #     count: int = 0
    #     for j in nanobots_bounds:
    #         intersection = bounds.intersection(j)
    #         if intersection.valid():
    #             count += 1
    #             bounds = intersection
    #     overlap.append((count, intersection))

    # overlap.sort(key=lambda k: k[0])

    # print(tuple(map(sub, overlap[-1][1].max, overlap[-1][1].min)))

    x = sorted(set((sum(int(abs(i[0][0] - j[0][0]) <= i[1]/2) for i in nanobots), j[0][0]) for j in nanobots), key=lambda k: k[0], reverse=True)
    y = sorted(set((sum(int(abs(i[0][1] - j[0][1]) <= i[1]/2) for i in nanobots), j[0][1]) for j in nanobots), key=lambda k: k[0], reverse=True)
    z = sorted(set((sum(int(abs(i[0][2] - j[0][2]) <= i[1]/2) for i in nanobots), j[0][2]) for j in nanobots), key=lambda k: k[0], reverse=True)

    in_range = (124572930, 126853300)

    a = []
    top = 0
    for u in range(len(x)):
        for v, w in product(range(min(u+1, len(y))), range(min(u+1, len(z)))):
            if not in_range[0] < abs(x[u][1]) + abs(y[v][1]) + abs(z[w][1]) < in_range[1]:
                continue
            c = sum(int(sum(map(lambda a, b: abs(a - b), (x[u][1], y[v][1], z[w][1]), b[0])) <= b[1]) for b in nanobots)
            a.append((c, (x[u][1], y[v][1], z[w][1])))
            if c > top:
                print((c, (x[u][1], y[v][1], z[w][1])))
                top = c
            # print((x[u][1], y[v][1], z[w][1]), c)

    a.sort(key=lambda k: k[0], reverse=True)

    pprint(a)

    return 0


def _count_overlap(nanobots) -> int:
    return sum(
        int(sum(map(lambda a, b: abs(a - b), i[0], j[0])) <= (i[1] + j[1]) / 2)
        for i in nanobots
        for j in nanobots
    )


def _count_in_range(nanobots, coordinates) -> int:
    return sum(
        int(sum(map(lambda a, b: abs(a - b), coordinates, nanobot[0])) <= nanobot[1])
        for nanobot in nanobots
    )


def _sample_range(nanobots, min_coordinate, max_coordinate, num_samples: int = 4) -> List[int]:
    sampling_interval = tuple(map(lambda a, b: int((b - a) / (num_samples + 1)), min_coordinate, max_coordinate))
    print(sampling_interval)
    samples = [
        _count_in_range(nanobots, (x, y, z))
        for x in range(min_coordinate[0] + int(sampling_interval[0]/2), max_coordinate[0] - int(sampling_interval[0]/2) + 1, max(sampling_interval[0], 1))
        for y in range(min_coordinate[1] + int(sampling_interval[1]/2), max_coordinate[1] - int(sampling_interval[1]/2) + 1, max(sampling_interval[1], 1))
        for z in range(min_coordinate[2] + int(sampling_interval[2]/2), max_coordinate[2] - int(sampling_interval[2]/2) + 1, max(sampling_interval[2], 1))
    ]
    print(samples)
    return samples


def _alternate_sample_range(nanobots, left_coordinate, right_coordinate, num_samples: int = 35):
    num_nanobots = len(nanobots)
    samples = []
    num_samples = num_nanobots * 6
    for i in range(num_samples):
        nanobot = nanobots[randrange(0, num_nanobots)]
        first = randrange(0, nanobot[1] + 1)
        second = randrange(0, nanobot[1] - first + 1)
        third = nanobot[1] - first - second
        location = tuple(map(add, nanobot[0], (first, second, third)))

        location = tuple(max(min(location[i], right_coordinate[i] - 1), left_coordinate[i]) for i in range(3))

        samples.append(_count_in_range(nanobots, location))

    return samples


def _search_axis(axis, left_coordinate, right_coordinate, nanobots):
    if sum(map(abs, map(sub, left_coordinate, right_coordinate))) <= 3:
        return left_coordinate

    comparison = int((left_coordinate[axis] + right_coordinate[axis]) / 2)

    left = [b for b in nanobots if b[0][axis] - b[1] <= comparison]
    right = [b for b in nanobots if b[0][axis] + b[1] >= comparison]
    # left_overlap = _count_overlap(left)
    # right_overlap = _count_overlap(right)

    left_range = (left_coordinate, tuple(comparison if i == axis else right_coordinate[i] for i in range(3)))
    right_range = (tuple(comparison if i == axis else left_coordinate[i] for i in range(3)), right_coordinate)

    # print(left_range, right_range)

    # left_sample = max(_sample_range(left, left_range[0], left_range[1], 16))
    # right_sample = max(_sample_range(right, right_range[0], right_range[1], 16))

    left_sample = max(_alternate_sample_range(left, left_range[0], left_range[1]))
    right_sample = max(_alternate_sample_range(right, right_range[0], right_range[1]))

    if left_sample > right_sample:
        return _search_axis((axis + 1) % 3, left_range[0], left_range[1], left)
    else:
        return _search_axis((axis + 1) % 3, right_range[0], right_range[1], right)


def _nanobots_range(nanobots):
    min_ = (min(b[0][0] - b[1] for b in nanobots), min(b[0][1] - b[1] for b in nanobots), min(b[0][2] - b[1] for b in nanobots))
    max_ = (max(b[0][0] + b[1] for b in nanobots), max(b[0][1] + b[1] for b in nanobots), max(b[0][2] + b[1] for b in nanobots))

    return min_, max_


def part2(coordinate_text: str) -> int:
    nanobots = _parse_coordinate_text(coordinate_text)

    search_range = _nanobots_range(nanobots)

    coordinate = _search_axis(0, search_range[0], search_range[1], nanobots)

    c = sum(int(sum(map(lambda a, b: abs(a - b), coordinate, b[0])) <= b[1]) for b in nanobots)
    print(c, coordinate)

    return sum(abs(i) for i in coordinate)
