# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import namedtuple
from re import match

from typing import Tuple, List, Dict


class Unit(namedtuple("Unit", ['size', 'hit_points', 'initiative', 'damage', 'type', 'immunities', 'weaknesses'])):
    @property
    def effective_strength(self):
        return self.size * self.damage

    @property
    def attack_order(self):
        return self.effective_strength, self.initiative

    def _attack_multiplier(self, attacker):
        if attacker.type in self.weaknesses:
            return 2
        elif attacker.type in self.immunities:
            return 0
        else:
            return 1

    def effective_damage(self, defender: 'Unit') -> int:
        if not isinstance(defender, Unit):
            raise ValueError('defender must be type Unit')
        return defender._attack_multiplier(self) * self.effective_strength

    def defend_order(self, attacker: 'Unit') -> Tuple[int, int, int]:
        if not isinstance(attacker, Unit):
            raise ValueError('defender must be type Unit')
        return attacker.effective_damage(self), self.effective_strength, self.initiative


def parse_unit_description(unit_description: str) -> Unit:
    unit_regex = r"(\d+) units each with (\d+) hit points (\([^\)]+\) )?" \
                 r"with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    effects_regex = r"(immune|weak) to (.*)"

    immunities = []
    weaknesses = []

    unit_group = match(unit_regex, unit_description)
    if unit_group[3]:
        for effects in unit_group[3].strip('() ').split('; '):
            effects_group = match(effects_regex, effects)
            if effects_group[1] == 'immune':
                immunities += effects_group[2].split(', ')
            elif effects_group[1] == 'weak':
                weaknesses += effects_group[2].split(', ')

    return Unit(int(unit_group[1]), int(unit_group[2]), int(unit_group[6]), int(unit_group[4]), unit_group[5],
                frozenset(immunities), frozenset(weaknesses))


def parse(description: str) -> Tuple[List[Unit], List[Unit]]:
    immune = []
    infection = []

    team = None
    for line in description.splitlines():
        if line.startswith('Immune System'):
            team = immune
        elif line.startswith('Infection'):
            team = infection
        else:
            if len(line) == 0:
                continue
            team.append(parse_unit_description(line))

    return immune, infection


def choose_targets(immune: List[Unit], infection: List[Unit]) -> Dict[Unit, Unit]:
    r = {}

    def _add_attackers(attackers, defenders):
        targets = defenders.copy()

        for attacker in sorted(attackers, key=lambda k: k.attack_order, reverse=True):
            targets.sort(key=lambda k: k.defend_order(attacker))
            if len(targets) > 0 and attacker.effective_damage(targets[-1]) > 0:
                r[attacker] = targets.pop()

    _add_attackers(infection, immune)
    _add_attackers(immune, infection)

    return r


def part1(description: str) -> int:
    immune, infection = parse(description)

    immune, infection = _simulate_battle(immune, infection)

    return max(sum(i.size for i in immune), sum(i.size for i in infection))


def _simulate_battle(immune, infection):
    # Continue battle
    while immune and infection:
        targets = choose_targets(immune, infection)
        if not targets:
            # Stalemate
            break
        # Simulate fight
        for initiative in sorted([attacker.initiative for attacker in targets.keys()], reverse=True):
            casualties = {}
            for attacker, defender in [target for target in targets.items() if target[0].initiative == initiative]:
                # Calculate damage to defender, add to casualties list
                damage = attacker.effective_damage(defender)
                units_killed = min(defender.size, int(damage / defender.hit_points))
                if units_killed > 0:
                    casualties[defender] = Unit(defender.size - units_killed,
                                                defender.hit_points,
                                                defender.initiative,
                                                defender.damage,
                                                defender.type,
                                                defender.immunities,
                                                defender.weaknesses)
            # Update target list based on casualties
            for unit in casualties:
                update = immune if unit in immune else infection
                if casualties[unit].size > 0:
                    if unit in targets:
                        targets[casualties[unit]] = targets[unit]
                    update.append(casualties[unit])
                if unit in targets:
                    del targets[unit]
                update.remove(unit)

    return immune, infection


def part2(description: str) -> int:
    immune, infection = parse(description)

    boosted_immune, remaining_infection = None, None
    search = range(1, 1_000_000)
    while len(search) > 1:
        boost = int((search.start + search.stop) / 2)
        boosted_immune = [
            Unit(unit.size,
                 unit.hit_points,
                 unit.initiative,
                 unit.damage + boost,
                 unit.type,
                 unit.immunities,
                 unit.weaknesses)
            for unit in immune
        ]
        boosted_immune, remaining_infection = _simulate_battle(boosted_immune, infection.copy())
        if remaining_infection:
            search = range(boost, search.stop)
        else:
            search = range(search.start, boost)

    if remaining_infection:
        boosted_immune = [
            Unit(unit.size,
                 unit.hit_points,
                 unit.initiative,
                 unit.damage + search.stop,
                 unit.type,
                 unit.immunities,
                 unit.weaknesses)
            for unit in immune
        ]
        boosted_immune, remaining_infection = _simulate_battle(boosted_immune, infection.copy())

    return sum(unit.size for unit in boosted_immune)
