# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import deque
from typing import List, Set, Dict


class Vector(object):

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __lt__(self, other: 'Vector') -> bool:
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other: 'Vector') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


# Movement/search directions in sort order
DIRECTIONS: List[Vector] = [Vector(0, -1), Vector(-1, 0), Vector(1, 0), Vector(0, 1)]


class Actor(object):

    def __init__(self, hit_points: int, allegiance: str, x: int, y: int, attack_power: int = 3) -> None:
        super().__init__()
        self.hit_points: int = hit_points
        self.allegiance: str = allegiance
        self.attack_power: int = attack_power
        self.pos: Vector = Vector(x, y)

    def distance(self, other) -> int:
        return self.pos.distance(other.pos)

    def in_range(self, other) -> bool:
        return self.distance(other) == 1

    def is_enemy(self, other) -> bool:
        return self.allegiance != other.allegiance

    def __lt__(self, other) -> bool:
        return self.pos < other.pos

    def attack(self, other: 'Actor') -> None:
        # FIXME: Assuming that we are in range/correct target
        other.take_damage(self.attack_power)

    def take_damage(self, damage_amount):
        self.hit_points -= damage_amount

    def move(self, vector: Vector) -> None:
        self.pos = self.pos + vector

    @property
    def alive(self) -> bool:
        return self.hit_points > 0

    @property
    def adjacent(self):
        return [self.pos + d for d in DIRECTIONS]

    def __repr__(self) -> str:
        return f"{self.allegiance}({self.hit_points})"


class Battle(object):

    def __init__(self, battle_map_text: str, elf_attack_power=3) -> None:
        super().__init__()
        self.round = 0
        self.actors = {
            Vector(x, y): Actor(200, tile, x, y, elf_attack_power if tile == 'E' else 3)
            for y, row in enumerate(battle_map_text.strip().splitlines())
            for x, tile in enumerate(row)
            if tile in ['G', 'E']
        }
        self.casualties: Dict[Vector, Actor] = {}
        self.map = [
            ''.join({
                'G': '.',
                'E': '.',
                '#': '#',
                '.': '.',
            }[tile] for tile in row)
            for row in battle_map_text.strip().splitlines()
        ]

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                self.actors[Vector(x, y)].allegiance if Vector(x, y) in self.actors else tile
                for x, tile in enumerate(row)
            )
            for y, row in enumerate(self.map)
        )

    def is_empty(self, vector):
        return vector not in self.actors and self.map[vector.y][vector.x] != '#'

    def move(self, actor, direction) -> None:
        del self.actors[actor.pos]
        actor.move(direction)
        self.actors[actor.pos] = actor

    def attack(self, actor: Actor, target: Actor) -> None:
        actor.attack(target)
        if not target.alive:
            del self.actors[target.pos]
            self.casualties[target.pos] = target

    @property
    def outcome(self):
        return self.round * sum(actor.hit_points for actor in self.actors.values())

    def simulate(self):
        def _nearest_movement_direction(point: Vector, targets: Set[Vector]):
            """Flood fill to find nearest target, search breadth first"""

            seen_points = {point}

            # Ultimately the result depends on our initial direction
            search_queue = deque(
                (point + dir_, dir_)
                for dir_ in DIRECTIONS
                if self.is_empty(point + dir_)
            )
            seen_points.update(point + dir_ for dir_ in DIRECTIONS)

            while search_queue:
                search_point, initial_dir = search_queue.popleft()
                if search_point in targets:
                    return initial_dir
                next_search_points = [search_point + dir_ for dir_ in DIRECTIONS]
                search_queue.extend(
                    (p, initial_dir)
                    for p in next_search_points
                    if p not in seen_points and self.is_empty(p)
                )
                seen_points.update(next_search_points)

            return None

        while True:
            for this in sorted(self.actors.values()):
                if not this.alive:
                    # Ignore dead people
                    continue

                # Find enemies
                enemies = sorted(other for other in self.actors.values() if this.is_enemy(other))
                if not enemies:
                    # No more enemies? Finish
                    return

                # Any in range?
                in_range = sorted((other for other in enemies if this.in_range(other)), key=lambda k: k.hit_points)

                # Otherwise move
                if not in_range:
                    # Of all enemies, what spaces do we want to occupy?
                    movement_target = set(
                        space
                        for enemy in enemies
                        for space in enemy.adjacent
                        if self.is_empty(space)
                    )
                    if movement_target:
                        direction = _nearest_movement_direction(this.pos, movement_target)
                        if direction:
                            self.move(this, direction)

                            # Recalculate in_range after moving
                            in_range = sorted((other for other in enemies if this.in_range(other)),
                                              key=lambda k: k.hit_points)

                # Any in range? Attack!
                if in_range:
                    self.attack(this, in_range[0])

            self.round += 1


def part1(battle_map_text: str) -> int:
    battle = Battle(battle_map_text)
    battle.simulate()

    return battle.outcome


def part2(battle_map_text: str) -> int:
    # Somewhere between incrementally more, and you will die when I touch you (but not over 9000!)
    power_range = (4, 200)

    while power_range[1] - power_range[0] > 1:
        power_level = int((power_range[0] + power_range[1]) / 2)

        battle = Battle(battle_map_text, power_level)
        battle.simulate()

        if any(dead.allegiance == 'E' for dead in battle.casualties.values()):
            power_range = (power_level, power_range[1])
        else:
            power_range = (power_range[0], power_level)

    battle = Battle(battle_map_text, power_range[1])
    battle.simulate()

    return battle.outcome
