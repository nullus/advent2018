# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.immune_system_simulator_20xx import parse_unit_description, parse, part1, Unit, choose_targets, part2
from advent.input import text

test_parse_unit_description_data = [
    [
        "2637 units each with 9485 hit points (immune to cold, slashing; weak to bludgeoning) with an attack that does 26 radiation damage at initiative 13",
        Unit(2637, 9485, 13, 26, "radiation", frozenset(["cold", "slashing"]), frozenset(["bludgeoning"])),
    ],
    [
        "120 units each with 53629 hit points with an attack that does 807 fire damage at initiative 15",
        Unit(120, 53629, 15, 807, "fire", frozenset(), frozenset()),
    ],
    [
        "9936 units each with 1739 hit points (weak to slashing, fire) with an attack that does 1 slashing damage at initiative 11",
        Unit(9936, 1739, 11, 1, "slashing", frozenset(), frozenset(["slashing", "fire"])),
    ],
]


@mark.parametrize("description, unit", test_parse_unit_description_data)
def test_parse_unit_description(description, unit):
    # Parse as units, hit points, initiative, damage, type, immunities, weaknesses
    assert unit == parse_unit_description(description)


test_data = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".strip()


def test_parse():
    immune, infection = parse(test_data)

    assert 2 == len(immune)
    assert 2 == len(infection)


def test_part1():
    assert 5216 == part1(test_data)


def test_target_defenders():
    immune, infection = parse(test_data)
    targets = choose_targets(immune, infection)
    # Infection group 2 attacks defending group 2, killing 84 units
    # Immune System group 2 attacks defending group 1, killing 4 units
    # Immune System group 1 attacks defending group 2, killing 51 units
    # Infection group 1 attacks defending group 1, killing 17 units
    assert targets[immune[1]] == infection[0]
    assert targets[immune[0]] == infection[1]
    assert targets[infection[0]] == immune[0]
    assert targets[infection[1]] == immune[1]


def test_unit_effective_strength():
    assert 65536 == Unit(256, 1, 2, 256, 'Potato', set(), set()).effective_strength


def test_part2_with_puzzle_input():
    assert 8291 == part2(text("immune_system_simulator_20xx"))
