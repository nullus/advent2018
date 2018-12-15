# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import deque
from functools import lru_cache


class Actor(object):

    def __init__(self, hit_points, allegiance, x, y, attack_power=3) -> None:
        super().__init__()
        self.hit_points = hit_points
        self.allegiance = allegiance
        self.attack_power = attack_power
        self.x = x
        self.y = y

    def distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def in_range(self, other) -> bool:
        return self.distance(other) == 1

    def is_enemy(self, other) -> bool:
        return self.allegiance != other.allegiance

    def __lt__(self, other) -> bool:
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def attack(self, other: 'Actor') -> None:
        # FIXME: Assuming that we are in range/correct target
        other.take_damage(self.attack_power)

    def take_damage(self, damage_amount):
        self.hit_points -= damage_amount

    @property
    def alive(self) -> bool:
        return self.hit_points > 0

    @property
    def adjacent(self):
        return [(self.x + d[0], self.y + d[1]) for d in [(0, -1), (-1, 0), (1, 0), (0, 1)]]

    def __repr__(self) -> str:
        return f"{self.allegiance}({self.hit_points})"


class Battle(object):

    def __init__(self, battle_map_text: str, elf_attack_power=3) -> None:
        super().__init__()
        self.round = 0
        self.actors = {
            (x, y): Actor(200, tile, x, y, elf_attack_power if tile == 'E' else 3)
            for y, row in enumerate(battle_map_text.strip().splitlines())
            for x, tile in enumerate(row)
            if tile in ['G', 'E']
        }
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
                self.actors[(x, y)].allegiance if (x, y) in self.actors else tile
                for x, tile in enumerate(row)
            )
            for y, row in enumerate(self.map)
        )

    def is_empty(self, x, y):
        return (x, y) not in self.actors and self.map[y][x] != '#'

    def simulate(self):
        def _nearest_movement_direction(point, targets):
            """Flood fill to find nearest target, search breadth first"""

            directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

            seen_points = {point}

            # Ultimately the result depends on our initial direction
            search_queue = deque(
                ((point[0] + dir_[0], point[1] + dir_[1]), dir_)
                for dir_ in directions
                if (point[0] + dir_[0], point[1] + dir_[1]) not in seen_points and self.is_empty(point[0] + dir_[0], point[1] + dir_[1])
            )
            seen_points.update((point[0] + dir_[0], point[1] + dir_[1]) for dir_ in directions)

            while search_queue:
                search_point, initial_dir = search_queue.popleft()
                if search_point in targets:
                    return initial_dir
                search_queue.extend(
                    ((search_point[0] + dir_[0], search_point[1] + dir_[1]), initial_dir)
                    for dir_ in directions
                    if (search_point[0] + dir_[0], search_point[1] + dir_[1]) not in seen_points and self.is_empty(search_point[0] + dir_[0], search_point[1] + dir_[1])
                )
                seen_points.update((search_point[0] + dir_[0], search_point[1] + dir_[1]) for dir_ in directions)

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
                    movement_target = frozenset([space for enemy in enemies for space in enemy.adjacent if self.is_empty(*space)])
                    if movement_target:
                        direction = _nearest_movement_direction((this.x, this.y), movement_target)
                        if direction:
                            del self.actors[(this.x, this.y)]
                            this.x += direction[0]
                            this.y += direction[1]
                            self.actors[(this.x, this.y)] = this

                            # Recalculate in_range after moving
                            in_range = sorted((other for other in enemies if this.in_range(other)),
                                              key=lambda k: k.hit_points)

                # Any in range? Attack!
                if in_range:
                    this.attack(in_range[0])
                    if not in_range[0].alive:
                        del self.actors[(in_range[0].x, in_range[0].y)]

            self.round += 1


def part1(battle_map_text: str) -> int:
    battle = Battle(battle_map_text)
    battle.simulate()

    return battle.round * sum(actor.hit_points for actor in battle.actors.values())


def part2(battle_map_text: str, elf_attack_power: int) -> int:
    battle = Battle(battle_map_text, elf_attack_power)
    battle.simulate()

    return battle.round * sum(actor.hit_points for actor in battle.actors.values())

