# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import cycle
from typing import Tuple, List, Set


class Cart(object):
    TURN_LEFT: int = -1
    GO_STRAIGHT: int = 0
    TURN_RIGHT: int = 1

    # Clockwise turning
    DIRECTIONS: List[str] = ['^', '>', 'v', '<']
    VECTOR: List[Tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, position: Tuple[int, int], direction: str) -> None:
        super().__init__()
        self.position: Tuple[int, int] = position
        self._direction: int = Cart.DIRECTIONS.index(direction)
        self._turn = cycle([Cart.TURN_LEFT, Cart.GO_STRAIGHT, Cart.TURN_RIGHT])

    def turn(self) -> None:
        next_turn = next(self._turn)
        self._direction = (self._direction + next_turn) % len(Cart.DIRECTIONS)

    def turn_corner(self, corner: str) -> None:
        self._direction = {
            '/':  {0: 1, 1: 0, 2: 3, 3: 2},
            '\\': {0: 3, 1: 2, 2: 1, 3: 0},
        }[corner][self._direction]

    def move(self) -> None:
        self.position = (
            self.position[0] + Cart.VECTOR[self._direction][0],
            self.position[1] + Cart.VECTOR[self._direction][1]
        )

    def act(self, tile: str) -> None:
        if tile in ['-', '|']:
            pass
        elif tile in ['/', '\\']:
            self.turn_corner(tile)
        elif tile == '+':
            self.turn()
        else:
            raise ValueError(f"We're in a bad place! Invalid tile (f{tile})")

    @property
    def direction(self):
        return Cart.DIRECTIONS[self._direction]

    def __repr__(self) -> str:
        return f"Cart(({repr(self.position)}, '{repr(self.direction)}')"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Cart):
            return False
        return (
            self.position[1] < other.position[1] or
            (self.position[1] == other.position[1] and self.position[0] < other.position[0])
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cart):
            return False
        return self.position[1] == other.position[1] and self.position[0] == other.position[0]

    def __hash__(self) -> int:
        return hash(self.position)


def _parser(track_text: str) -> Tuple[List[str], List[Cart]]:
    track: List[str] = []
    carts: List[Cart] = []

    # "Extract" carts from track
    for y, line in enumerate(track_text.splitlines()):
        row = []
        for x, tile in enumerate(line):
            if tile in ['<', '>', '^', 'v']:
                carts.append(Cart((x, y), tile))
                row.append({'<': '-', '>': '-', '^': '|', 'v': '|'}[tile])
            else:
                row.append(tile)
        track.append(''.join(row))

    return track, carts


def part1(track_text: str) -> Tuple[int, int]:
    track, carts = _parser(track_text)

    while True:
        positions: Set[Cart] = set(i for i in carts)
        for cart in sorted(carts):
            positions.remove(cart)
            cart.move()
            cart.act(track[cart.position[1]][cart.position[0]])
            if cart in positions:
                return cart.position
            positions.add(cart)


def part2(track_text: str) -> Tuple[int, int]:
    track, carts = _parser(track_text)

    while len(carts) > 1:
        positions: Set[Cart] = set(carts)
        for cart in sorted(carts):
            if cart not in positions:
                continue
            positions.remove(cart)
            cart.move()
            cart.act(track[cart.position[1]][cart.position[0]])
            # Test for collision
            if cart in positions:
                positions.remove(cart)
            else:
                positions.add(cart)
        carts = list(positions)

    return carts[0].position
