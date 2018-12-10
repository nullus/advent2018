# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import deque


def part1(players: int, last_marble: int) -> int:
    score = [0] * players

    player = 0
    circle = [0]
    current_position = 0

    for marble in range(1, last_marble + 1):
        if marble % 23:
            next_position = ((current_position + 1) % len(circle)) + 1
            circle.insert(next_position, marble)
            current_position = next_position
        else:
            # Is divisible
            next_position = ((current_position - 7) % len(circle))
            score[player] += circle[next_position] + marble
            del circle[next_position]
            current_position = next_position

        player = (player + 1) % len(score)

    return max(score)


def part2(players: int, last_marble: int) -> int:
    score = [0] * players

    player = 22 % players
    circle = deque([0])

    for marble in range(1, 23):
        circle.rotate(1)
        circle.appendleft(marble)

    for scoring_marble in range(23, last_marble + 1, 23):
        circle.rotate(-7)
        score[player] += circle.popleft() + scoring_marble
        circle.rotate(1)

        for marble in range(1, 23):
            circle.rotate(1)
            circle.appendleft(scoring_marble + marble)

        player = (player + 23) % players

    return max(score)
