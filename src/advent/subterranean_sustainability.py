# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict, deque
from itertools import chain, count
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


def _next_state(state: List[bool], rules: Dict[Tuple[bool, ...], bool], offset: int = 0) -> Tuple[List[bool], int]:
    # Use fixed size deque and chain to window over state
    def window_state(window_size: int = 5):
        padding: List[bool] = [False] * (window_size - 1)
        state_padded: Iterator[bool] = chain(state, padding)
        window: deque[bool] = deque(padding, maxlen=window_size)
        for elem in state_padded:
            window.append(elem)
            yield tuple(window)

    next_state: List[bool] = [rules[i] for i in window_state(5)]
    first_true: int = next_state.index(True)
    last_true: int = next(1 - i for i in count(1) if next_state[-i])

    return next_state[first_true:last_true], offset - 2 + first_true


def _print_state(state: List[bool]):
    print(''.join({True: '#', False: '.'}[i] for i in state))


def _final_state(state: List[bool], rules: Dict[Tuple[bool, ...], bool], generations: int) -> Tuple[List[bool], int]:
    offset: int = 0
    for generation in range(generations):
        next_state, next_offset = _next_state(state, rules, offset)
        if next_state == state:
            # Calculate final offset and return if we reach a stable state
            return state, offset + (next_offset - offset) * (generations - generation)
        state, offset = next_state, next_offset

    return state, offset


def answer(growth_rules: str, generations: int) -> int:
    state, rules = _parser(growth_rules)
    final_state, offset = _final_state(state, rules, generations)

    return sum((i + offset) for i in range(0, len(final_state)) if final_state[i])
