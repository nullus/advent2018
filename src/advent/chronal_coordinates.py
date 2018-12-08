# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict
from typing import Iterator, Tuple, List


def text_to_points(text: str) -> Iterator[Tuple[int, int]]:
    for i in text.strip().splitlines():
        yield tuple(int(i) for i in i.split(", "))


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def inside(a: Tuple[int, int], low: Tuple[int, int], high: Tuple[int, int]) -> bool:
    return low[0] < a[0] < high[0] and low[1] < a[1] < high[1]


def part1(input_text: str) -> int:
    points = list(text_to_points(input_text))

    bound_low = min(points, key=lambda k: k[0])[0], min(points, key=lambda k: k[1])[1]
    bound_high = max(points, key=lambda k: k[0])[0], max(points, key=lambda k: k[1])[1]

    inside_points = [i for i, point in enumerate(points) if inside(point, bound_low, bound_high)]

    point_area = defaultdict(lambda: 0)

    for y in range(bound_low[1], bound_high[1] + 1):
        for x in range(bound_low[0], bound_high[0] + 1):
            distances = sorted([(manhattan((x, y), point), i) for i, point in enumerate(points)], key=lambda k: k[0])
            # Check whether the point is inside the bounds, anything that isn't will be infinite
            if inside((x, y), bound_low, bound_high):
                if distances[0][0] < distances[1][0] and distances[0][1] in inside_points:
                    point_area[distances[0][1]] += 1
            else:
                if distances[0][1] in inside_points:
                    del inside_points[inside_points.index(distances[0][1])]
                    point_area[distances[0][1]] = 0

    return max(point_area.items(), key=lambda k: k[1])[1]


def part2(input_text: str, threshold: int) -> int:
    points = list(text_to_points(input_text))

    bound_low = min(points, key=lambda k: k[0])[0], min(points, key=lambda k: k[1])[1]
    bound_high = max(points, key=lambda k: k[0])[0], max(points, key=lambda k: k[1])[1]

    distance_total: List[List[int]] = []

    for y in range(bound_low[1], bound_high[1] + 1):
        distance_total.append([0] * (bound_high[0] - bound_low[0] + 1))
        for x in range(bound_low[0], bound_high[0] + 1):
            if distance_total[y - bound_low[1]][x - bound_low[0]] < threshold:
                distance_total[y - bound_low[1]][x - bound_low[0]] += sum(
                    manhattan((x, y), point) for point in points
                )

    return sum([len([i for i in row if i < threshold]) for row in distance_total])
