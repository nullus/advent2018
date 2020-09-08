# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import cycle
from math import ceil
from operator import sub
from typing import Tuple, List, Set, Iterator, NamedTuple, Optional


class Vector(NamedTuple):
    # Preserve ordering to maintain
    y: int
    x: int

    def __sub__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise ValueError(f"Expected type {Vector}, got {type(other)}")
        return Vector(*map(sub, self, other))


class Body(object):

    def __init__(self, position: Vector, velocity: Vector = Vector(0, 0)) -> None:
        super().__init__()

        self.position = position
        self.velocity = velocity

    def collision_time(self, other: 'Body') -> Optional[int]:
        """
        Solve collision as complex division between origin and velocity deltas

        Positive, real result indicates time of collision. Otherwise return None
        """

        if not isinstance(other, Body):
            raise ValueError(f"Expected type {Body}, got {type(other)}")

        delta_origin = other.position - self.position
        delta_velocity = self.velocity - other.velocity

        denominator = delta_velocity.x * delta_velocity.x + delta_velocity.y * delta_velocity.y
        real = delta_origin.x * delta_velocity.x + delta_origin.y * delta_velocity.y
        imaginary = delta_origin.y * delta_velocity.x - delta_origin.x * delta_velocity.y

        if denominator != 0 and imaginary == 0 and real > 0:
            return ceil(real / denominator)
        else:
            return None


class Event(object):

    def __init__(self, position: Vector, tick: int) -> None:
        super().__init__()

        self.tick = tick
        self.position = position

    def __lt__(self, other: object) -> bool:
        return isinstance(other, Event) and self._id() < other._id()

    def _id(self) -> Tuple[int, Vector]:
        return self.tick, self.position


class Turn(object):
    pass


class Simulation(object):




class Cart(object):
    TURN_LEFT: int = -1
    GO_STRAIGHT: int = 0
    TURN_RIGHT: int = 1

    # Clockwise turning to match turn direction above
    DIRECTIONS: List[str] = ['^', '>', 'v', '<']
    VELOCITY: List[Tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, position: Tuple[int, int], direction: str) -> None:
        super().__init__()
        self.position: Tuple[int, int] = position
        self._direction: int = Cart.DIRECTIONS.index(direction)
        self._turn = cycle([Cart.TURN_LEFT, Cart.GO_STRAIGHT, Cart.TURN_RIGHT])

    def move(self) -> None:
        self.position = (
            self.position[0] + Cart.VELOCITY[self._direction][0],
            self.position[1] + Cart.VELOCITY[self._direction][1]
        )

    def act(self, tile: str) -> None:
        if tile in ['-', '|']:
            pass
        elif tile in ['/', '\\']:
            self._direction = {
                '/':  {0: 1, 1: 0, 2: 3, 3: 2},
                '\\': {0: 3, 1: 2, 2: 1, 3: 0},
            }[tile][self._direction]
        elif tile == '+':
            self._direction = (self._direction + next(self._turn)) % len(Cart.DIRECTIONS)
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


def _parser(track_text: str) -> Tuple[List[str], Set[Cart]]:
    track: List[str] = []
    carts: Set[Cart] = set()

    # "Extract" carts from track
    for y, line in enumerate(track_text.splitlines()):
        row = []
        for x, tile in enumerate(line):
            if tile in ['<', '>', '^', 'v']:
                carts.add(Cart((x, y), tile))
                row.append({'<': '-', '>': '-', '^': '|', 'v': '|'}[tile])
            else:
                row.append(tile)
        track.append(''.join(row))

    return track, carts


def _collisions(track: List[str], carts: Set[Cart]) -> Iterator[Tuple[int, int]]:
    while len(carts) > 1:
        for cart in sorted(carts):
            if cart not in carts:
                # Already collided
                continue
            # Remove to mutating the cart and breaking the set invariant (feels dirty)
            carts.remove(cart)
            cart.move()
            cart.act(track[cart.position[1]][cart.position[0]])
            # Test for collisions
            if cart in carts:
                # Collided
                carts.remove(cart)
                yield cart.position
            else:
                # Add back to set
                carts.add(cart)

    # This will raise if the set is empty
    yield carts.pop().position


def part1(track_text: str) -> Tuple[int, int]:
    track, carts = _parser(track_text)

    return next(_collisions(track, carts))


def part2(track_text: str) -> Tuple[int, int]:
    track, carts = _parser(track_text)

    return list(_collisions(track, carts))[-1]
