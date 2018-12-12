# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict, deque
from itertools import chain
from typing import List, Dict, Tuple, Iterator


def _parser(growth_rules: str) -> Tuple[List[bool], Dict[Tuple[bool, ...], bool]]:
    initial_state: List[bool] = []
    rules: Dict[Tuple[bool, ...]] = defaultdict(lambda: False)
    for i, line in enumerate(growth_rules.splitlines()):
        if i == 0:
            initial_state = [i == '#' for i in line[15:]]
        elif i > 1:
            rules[tuple(i == '#' for i in line[:5])] = line[-1] == '#'
    return initial_state, rules


def _next_state(state: List[bool], rules: Dict[Tuple[bool, ...], bool], offset: int = 0) -> List[bool]:
    # Use fixed size deque and chain to window over state
    def window_state(window_size: int = 5):
        padding: List[bool] = [False] * (window_size - 1)
        state_padded: Iterator[bool] = chain(state, padding)
        window: deque[bool] = deque(padding, maxlen=window_size)
        for elem in state_padded:
            window.append(elem)
            yield tuple(window)

    next_state: List[bool] = [rules[i] for i in window_state(5)]

    return next_state


def _print_state(state: List[bool]):
    print(''.join({True: '#', False: '.'}[i] for i in state))


def part1(growth_rules: str) -> int:
    state, rules = _parser(growth_rules)
    left_index: int = 0
    for generation in range(20):
        state = _next_state(state, rules)
        left_index += -2 + state.index(True)
        state = state[state.index(True):]

    return sum((i + left_index) for i in range(0, len(state)) if state[i])


def part2(growth_rules: str) -> int:
    state, rules = _parser(growth_rules)
    left_index: int = 0
    for generation in range(200):
        state = _next_state(state, rules)
        left_index += -2 + state.index(True)
        state = state[state.index(True):]

    return (50_000_000_000 - 200) * 38 + sum((i + left_index) for i in range(0, len(state)) if state[i])
