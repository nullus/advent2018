# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from math import inf
from operator import add
from typing import Tuple, Dict, Iterator

direction_to_vector = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
 }


def process_map_path(map_regex_iter: Iterator[str], map_nodes: Dict[Tuple[int, int], int],
                     start_location: Tuple[int, int], start_distance: int = 0) -> None:

    location = start_location
    distance = start_distance

    while True:
        try:
            token = next(map_regex_iter)
        except StopIteration:
            break
        if token in ('N', 'E', 'S', 'W'):
            # Next iteration of location data
            next_location: Tuple[int, int] = tuple(map(add, location, direction_to_vector[token]))
            map_nodes[next_location] = min(distance + 1, map_nodes.get(next_location, inf))
            distance += 1
            location = next_location
        elif token == '(':
            process_map_path(map_regex_iter, map_nodes, location, distance)
        elif token == '|':
            process_map_path(map_regex_iter, map_nodes, start_location, start_distance)
            break
        elif token == ')' or token == '$':
            break
        else:
            raise RuntimeError(f'Unexpected token: {token}')


def process_map_regex(map_regex_iter: Iterator[str]) -> Dict[Tuple[int, int], int]:
    while True:
        token = next(map_regex_iter)
        if token == '^':
            map_nodes = {}
            process_map_path(map_regex_iter, map_nodes, (0, 0))
            return map_nodes
        else:
            raise RuntimeError(f'Unexpected token: {token}')


def part1(map_regex: str) -> int:
    map_nodes = process_map_regex(iter(map_regex))
    max_node = max(map_nodes.values())
    return max_node


def part2(map_regex: str) -> int:
    map_nodes = process_map_regex(iter(map_regex))
    return len([i for i in map_nodes.values() if i >= 1000])
