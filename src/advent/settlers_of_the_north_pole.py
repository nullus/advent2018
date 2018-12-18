# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import product, count
from typing import List, Set, Tuple


def parse(input_map_str: str) -> List[List[str]]:
    return [
        [i for i in row]
        for row in input_map_str.splitlines()
    ]


def resource_value(map_: List[List[str]]) -> int:
    return sum(row.count('#') for row in map_) * sum(row.count('|') for row in map_)


def map_str(map_: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in map_)


def next_state(map_: List[List[str]]) -> List[List[str]]:
    next_map = []
    for y, row in enumerate(map_):
        next_row = []
        for x, tile in enumerate(row):
            surrounding_tiles = [
                map_[v][u]
                for u, v in product(range(x - 1, x + 2), range(y - 1, y + 2))
                if (u, v) != (x, y) and 0 <= u < len(row) and 0 <= v < len(map_)
            ]
            if tile == '.' and surrounding_tiles.count('|') >= 3:
                next_row.append('|')
            elif tile == '|' and surrounding_tiles.count('#') >= 3:
                next_row.append('#')
            elif tile == '#' and not (surrounding_tiles.count('#') >= 1 and surrounding_tiles.count('|') >= 1):
                next_row.append('.')
            else:
                next_row.append(tile)
        next_map.append(next_row)

    return next_map


def part1(input_map_str: str) -> int:
    map_ = parse(input_map_str)

    for i in range(10):
        map_ = next_state(map_)

    return resource_value(map_)


def part2(input_map_str: str, minutes: int) -> int:
    map_ = parse(input_map_str)
    history: List[str] = [input_map_str.strip()]
    map_history: Set[str] = {input_map_str.strip()}
    i: int = 0
    for i in range(minutes):
        map_ = next_state(map_)
        map_serialised = map_str(map_)
        if map_serialised in map_history:
            break
        map_history.add(map_serialised)
        history.append(map_serialised)

    first_index = history.index(map_str(map_))
    return resource_value(parse(history[first_index + (minutes - i - 1) % (len(history) - first_index)]))
