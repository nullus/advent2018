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
        print(f"{self} attacks {other}")
        other.take_damage(self.attack_power)

    def take_damage(self, damage_amount):
        print(f"{self} takes {damage_amount} damage")
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
        # A dict for out of work actors :P
        self.stuck = set()
        self.map = [
            ''.join({
                'G': '.',
                'E': '.',
                '#': '#',
                '.': '.',
            }[tile] for tile in row)
            for row in battle_map_text.strip().splitlines()
        ]
        self.map_blocked_points = set([
            (x, y)
            for y, row in enumerate(self.map)
            for x, tile in enumerate(row)
            if tile == '#'
        ])

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
        # @lru_cache(128)
        def _nearest_movement_direction(point, targets, invalid_points=None):
            """Flood fill to find nearest target, search breadth first"""

            directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

            seen_points = {point}
            if invalid_points:
                seen_points = seen_points.union(invalid_points)

            # Ultimately the result depends on our initial direction, and distance
            search_queue = deque(
                ((point[0] + dir_[0], point[1] + dir_[1]), dir_, 1)
                for dir_ in directions
                if (point[0] + dir_[0], point[1] + dir_[1]) not in seen_points
            )
            seen_points.update((point[0] + dir_[0], point[1] + dir_[1]) for dir_ in directions)

            while search_queue:
                search_point, initial_dir, distance = search_queue.popleft()
                # seen_points.add(search_point)
                if search_point in targets:
                    print(f"found")
                    return initial_dir
                search_queue.extend(
                    ((search_point[0] + dir_[0], search_point[1] + dir_[1]), initial_dir, distance + 1)
                    for dir_ in directions
                    if (search_point[0] + dir_[0], search_point[1] + dir_[1]) not in seen_points
                )
                seen_points.update((search_point[0] + dir_[0], search_point[1] + dir_[1]) for dir_ in directions)

            return None

        while True:
            print(self.round)
            print(str(self))
            print(self.actors)
            for this in sorted(self.actors.values()):
                if not this.alive:
                    # Ignore dead people
                    continue

                # find enemies
                enemies = sorted(other for other in self.actors.values() if this.is_enemy(other))
                if not enemies:
                    # No more enemies? Finish
                    return

                # any in range? attack
                in_range = sorted((other for other in enemies if this.in_range(other)), key=lambda k: k.hit_points)
                if in_range:
                    this.attack(in_range[0])
                    if not in_range[0].alive:
                        print(f"{in_range[0]} dies")
                        if in_range[0].allegiance == 'E':
                            print("Oh noes! it was a elf")
                            return
                        del self.actors[(in_range[0].x, in_range[0].y)]
                        # Unstick actors
                        self.stuck = set()

                # otherwise move
                else:
                    # Of all enemies, what spaces do we want to occupy?
                    movement_target = frozenset([space for enemy in enemies for space in enemy.adjacent if self.is_empty(*space)])
                    if (this.x, this.y) not in self.stuck and movement_target:
                        print(f"{this} finding a place to move")
                        direction = _nearest_movement_direction((this.x, this.y), movement_target, frozenset(self.map_blocked_points.union(self.actors.keys())))
                        if direction:
                            print(f"{this} moves {direction}")
                            del self.actors[(this.x, this.y)]
                            this.x += direction[0]
                            this.y += direction[1]
                            self.actors[(this.x, this.y)] = this
                            # Unstick actors
                            self.stuck = set()
                        else:
                            # A failure to move means we probably can't move until someone dies/moves: flag it
                            print(f"{this} is stuck")
                            self.stuck.add((this.x, this.y))

                    # any in range? attack
                    in_range = sorted((other for other in enemies if this.in_range(other)), key=lambda k: k.hit_points)
                    if in_range:
                        this.attack(in_range[0])
                        if not in_range[0].alive:
                            print(f"{in_range[0]} dies")
                            del self.actors[(in_range[0].x, in_range[0].y)]
                            # Unstick actors
                            self.stuck = set()

            self.round += 1


def part1(battle_map_text: str) -> int:
    battle = Battle(battle_map_text)
    battle.simulate()
    print(battle.round, sum(actor.hit_points for actor in battle.actors.values()))

    return battle.round * sum(actor.hit_points for actor in battle.actors.values())


def part2(battle_map_text: str, elf_attack_power: int) -> int:
    battle = Battle(battle_map_text, elf_attack_power)
    battle.simulate()
    print(battle.round, sum(actor.hit_points for actor in battle.actors.values()))

    return battle.round * sum(actor.hit_points for actor in battle.actors.values())

