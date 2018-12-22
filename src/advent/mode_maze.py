# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from functools import lru_cache
from heapq import heappush, heappop
from operator import sub, add
from typing import Tuple, List


@lru_cache(maxsize=262_144)
def erosion_level(coords: Tuple[int, int], depth: int) -> int:
    return (geologic_index(coords, depth) + depth) % 20183


@lru_cache(maxsize=262_144)
def geologic_index(coords: Tuple[int, int], depth: int) -> int:
    if coords[0] == 0:
        return coords[1] * 48271
    elif coords[1] == 0:
        return coords[0] * 16807
    else:
        return (
            erosion_level(tuple(map(sub, coords, (1, 0))), depth) *
            erosion_level(tuple(map(sub, coords, (0, 1))), depth)
        )


def part1(coords: Tuple[int, int], depth: int) -> int:
    return sum(
        erosion_level((x, y), depth) % 3
        for y in range(0, coords[1] + 1)
        for x in range(0, coords[0] + 1)
        if (x, y) != coords
    )


def _valid_tools(location: Tuple[int, int], depth: int, target: Tuple[int, int]) -> List[str]:
    if location == target:
        return ['climbing gear', 'torch']

    return [
        # rocky
        ['climbing gear', 'torch'],
        # wet
        ['none', 'climbing gear'],
        # narrow
        ['torch', 'none'],
    ][erosion_level(location, depth) % 3]


class Action(object):
    def __init__(self, minutes_elapsed, location, equipped, target) -> None:
        super().__init__()
        self.minutes_elapsed = minutes_elapsed
        self.location = location
        self.equipped = equipped
        self.target = target
        self.priority = self.minutes_elapsed + abs(self.target[0] - self.location[0]) + abs(self.target[1] - self.location[1])

    def __lt__(self, other):
        if not isinstance(other, Action):
            raise ValueError()
        return self.priority < other.priority


def part2(target: Tuple[int, int], depth: int) -> int:
    """
    Minimum number of minutes taken to reach target
    """

    action_queue = []
    previous_states = set()

    heappush(action_queue, Action(0, (0, 0), 'torch', target))

    while True:
        action = heappop(action_queue)

        previous_states.add((action.location, action.equipped))

        if action.location == target and action.equipped == 'torch':
            return action.minutes_elapsed

        next_actions = [
            # Next possible actions (movement)
            Action(action.minutes_elapsed + 1, next_location, action.equipped, action.target)
            for next_location in (
                tuple(map(add, action.location, direction))
                for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]
            )
            if (next_location[0] >= 0 and next_location[1] >= 0 and
                action.equipped in _valid_tools(next_location, depth, target) and
                (next_location, action.equipped) not in previous_states)
        ] + [
            # Next possible actions (equipment change)
            Action(action.minutes_elapsed + 7, action.location, next_equipped, action.target)
            for next_equipped in _valid_tools(action.location, depth, target)
            if (action.location, next_equipped) not in previous_states
        ]

        for i in next_actions:
            heappush(action_queue, i)
