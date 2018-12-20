# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict
from operator import add
from typing import List, Tuple, Dict, Iterator, Set


class Node(object):
    def __init__(self) -> None:
        super().__init__()
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        # Large enough for now
        self.distance = 0


direction_to_vector = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
 }


def process_map_path(map_regex_iter: Iterator[str], map_nodes: Dict[Tuple[int, int], Node],
                     start_locations: Set[Tuple[int, int]], start_distance: int = 0):

    locations = start_locations
    distance = start_distance

    while True:
        try:
            next_token = next(map_regex_iter)
        except StopIteration:
            return set()

        if next_token in ('N', 'E', 'S', 'W'):
            # Next iteration of location data
            next_locations: List[Tuple[int, int]] = [
                tuple(map(add, i, direction_to_vector[next_token]))
                for i in locations
            ]
            for location, next_location in zip(locations, next_locations):
                if map_nodes[next_location].distance:
                    map_nodes[next_location].distance = min(distance + 1, map_nodes[next_location].distance)
                else:
                    map_nodes[next_location].distance = distance + 1
                if next_token == 'N':
                    map_nodes[location].north = map_nodes[next_location]
                    map_nodes[next_location].south = map_nodes[location]
                elif next_token == 'E':
                    map_nodes[location].east = map_nodes[next_location]
                    map_nodes[next_location].west = map_nodes[location]
                elif next_token == 'S':
                    map_nodes[location].south = map_nodes[next_location]
                    map_nodes[next_location].north = map_nodes[location]
                elif next_token == 'W':
                    map_nodes[location].west = map_nodes[next_location]
                    map_nodes[next_location].east = map_nodes[location]
            distance += 1
            locations = set(next_locations)
        elif next_token == '(':
            locations = locations.union(process_map_path(map_regex_iter, map_nodes, locations, distance))
        elif next_token == '|':
            return locations.union(process_map_path(map_regex_iter, map_nodes, start_locations, start_distance))
        elif next_token == ')' or next_token == '$':
            return locations
        else:
            raise RuntimeError(f'Unexpected token: {next_token}')


def process_map_regex(map_regex_iter: Iterator[str]) -> Dict[Tuple[int, int], Node]:
    while True:
        next_token = next(map_regex_iter)
        if next_token == '^':
            map_nodes = defaultdict(lambda: Node())
            process_map_path(map_regex_iter, map_nodes, {(0, 0)})
            return map_nodes
        else:
            raise RuntimeError('Unexpected token')


def part1(map_regex: str) -> int:
    map_nodes = process_map_regex(iter(map_regex))

    max_node = max(map_nodes.values(), key=lambda x: x.distance)

    return max_node.distance


def part2(map_regex: str) -> int:
    map_nodes = process_map_regex(iter(map_regex))

    return len([i for i in map_nodes.values() if i.distance >= 1000])
