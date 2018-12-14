# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import deque

from typing import List, Tuple


def part1(initial_scores: List[int], attempted_recipes: int) -> str:
    scores: List[int] = initial_scores.copy()
    elf_recipe: List[int] = list(range(len(initial_scores)))

    while len(scores) < attempted_recipes + 10:
        scores += (int(i) for i in str(sum(scores[j] for j in elf_recipe)))
        elf_recipe = [(i + scores[i] + 1) % len(scores) for i in elf_recipe]

    return ''.join(str(i) for i in scores[attempted_recipes:attempted_recipes + 10])


def part2(initial_scores: List[int], match_sequence_str: str) -> int:
    scores: List[int] = initial_scores.copy()
    elf_recipe: Tuple[int, int] = (0, 1)
    match_sequence: deque[int] = deque(int(i) for i in match_sequence_str)
    sequence: deque[int] = deque(scores, maxlen=len(match_sequence_str))

    while True:
        for i, digit in enumerate(int(i) for i in str(scores[elf_recipe[0]] + scores[elf_recipe[1]])):
            sequence.append(digit)
            scores += [digit]
            if match_sequence == sequence:
                return len(scores) - len(match_sequence_str)
        elf_recipe = (
            (scores[elf_recipe[0]] + elf_recipe[0] + 1) % len(scores),
            (scores[elf_recipe[1]] + elf_recipe[1] + 1) % len(scores)
        )
