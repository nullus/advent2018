# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.


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


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def append(self, node):
        # Update new node
        node.prev, node.next = self, self.next
        # Update existing nodes
        node.prev.next, node.next.prev = node, node
        return node

    def remove(self):
        result = self.next
        # Update our neighbours
        self.next.prev, self.prev.next = self.prev, self.next
        # Remove ourselves
        self.next, self.prev = self, self
        # Return what _was_ next
        return result

    def advance(self, num_nodes):
        node = self
        if num_nodes >= 0:
            for i in range(num_nodes):
                node = node.next
        else:
            for i in range(-num_nodes):
                node = node.prev

        return node


def part2(players: int, last_marble: int) -> int:
    score = [0] * players

    player = 0
    circle = Node(0)

    for marble in range(1, last_marble + 1):
        if marble % 23:
            circle = circle.advance(1).append(Node(marble))
        else:
            circle = circle.advance(-7)
            score[player] += circle.value + marble
            old_circle = circle
            circle = circle.remove()
            del old_circle

        player = (player + 1) % len(score)

    return max(score)
