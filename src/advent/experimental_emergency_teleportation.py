# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from operator import sub, add
from random import randrange
from re import match


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


def _sample_range(nanobots, left_coordinate, right_coordinate):
    samples = []
    for i in range(len(nanobots) * 6):
        nanobot = nanobots[randrange(0, len(nanobots))]
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

    left_range = (left_coordinate, tuple(comparison if i == axis else right_coordinate[i] for i in range(3)))
    right_range = (tuple(comparison if i == axis else left_coordinate[i] for i in range(3)), right_coordinate)

    left_sample = max(_sample_range(left, left_range[0], left_range[1]))
    right_sample = max(_sample_range(right, right_range[0], right_range[1]))

    if left_sample > right_sample:
        return _search_axis((axis + 1) % 3, left_range[0], left_range[1], left)
    else:
        return _search_axis((axis + 1) % 3, right_range[0], right_range[1], right)


def _nanobots_range(nanobots):
    min_ = (
        min(b[0][0] - b[1] for b in nanobots),
        min(b[0][1] - b[1] for b in nanobots),
        min(b[0][2] - b[1] for b in nanobots)
    )

    max_ = (
        max(b[0][0] + b[1] for b in nanobots),
        max(b[0][1] + b[1] for b in nanobots),
        max(b[0][2] + b[1] for b in nanobots)
    )

    return min_, max_


def part2(coordinate_text: str) -> int:
    nanobots = _parse_coordinate_text(coordinate_text)

    search_range = _nanobots_range(nanobots)

    coordinate = _search_axis(0, search_range[0], search_range[1], nanobots)

    c = sum(int(sum(map(lambda a, b: abs(a - b), coordinate, b[0])) <= b[1]) for b in nanobots)
    print(c, coordinate)

    return sum(abs(i) for i in coordinate)
