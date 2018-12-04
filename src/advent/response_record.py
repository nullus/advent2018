# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.
from itertools import accumulate
from typing import Optional, List, Dict, Tuple


def part1(response_record_text: str) -> int:
    # Parsing input
    response_record = sorted(response_record_text.strip().splitlines())

    guard: int = None
    awake: Optional[bool] = True

    guard_total_sleep: Dict[int, int] = {}
    guard_sleep_times: Dict[int, List[Tuple[int, int]]] = {}

    for record in response_record:
        minutes: int = int(record[15:17])
        action: str = record[19:]

        if action.startswith('Guard'):
            assert awake
            guard = int(action[7:-13])
            if guard not in guard_total_sleep:
                guard_total_sleep[guard] = 0
                guard_sleep_times[guard] = []
        elif action.startswith('falls asleep'):
            assert guard is not None and awake
            guard_sleep_times[guard].append((minutes, 1))
            awake = False
        elif action.startswith('wakes up'):
            assert guard is not None and not awake
            guard_sleep_times[guard].append((minutes, -1))
            (m1, _), (m2, _) = guard_sleep_times[guard][-2:]
            guard_total_sleep[guard] += m2 - m1
            awake = True
        else:
            raise RuntimeError()

    sleepy_guard = sorted(((v, k) for k, v in guard_total_sleep.items()), key=lambda x: x[0], reverse=True)[0][1]

    cumulative_sleep = accumulate(sorted(guard_sleep_times[sleepy_guard], key=lambda x: x[0]), func=lambda a, b: (b[0], a[1] + b[1]))

    m1 = 60
    deepest = 0
    minutey = 0
    for m2, depth in reversed(list(cumulative_sleep)):
        if m2 < m1 and depth > deepest:
            print(m2, depth)
            deepest = depth
            minutey = m2
        m1 = m2

    return minutey * sleepy_guard


def part2(response_record_text: str) -> int:
    # Parsing input
    response_record = sorted(response_record_text.strip().splitlines())

    guard: int = None
    awake: Optional[bool] = True

    guard_total_sleep: Dict[int, int] = {}
    guard_sleep_times: Dict[int, List[Tuple[int, int]]] = {}

    for record in response_record:
        minutes: int = int(record[15:17])
        action: str = record[19:]

        if action.startswith('Guard'):
            assert awake
            guard = int(action[7:-13])
            if guard not in guard_total_sleep:
                guard_total_sleep[guard] = 0
                guard_sleep_times[guard] = []
        elif action.startswith('falls asleep'):
            assert guard is not None and awake
            guard_sleep_times[guard].append((minutes, 1))
            awake = False
        elif action.startswith('wakes up'):
            assert guard is not None and not awake
            guard_sleep_times[guard].append((minutes, -1))
            (m1, _), (m2, _) = guard_sleep_times[guard][-2:]
            guard_total_sleep[guard] += m2 - m1
            awake = True
        else:
            raise RuntimeError()

    longest_sleep: int = 0
    guard_id: int = 0
    sleeping_minute: int = 0

    for guard_number, guard_sleep_time in guard_sleep_times.items():

        cumulative_sleep = accumulate(sorted(guard_sleep_time, key=lambda x: x[0]),
                                      func=lambda a, b: (b[0], a[1] + b[1]))

        m1 = 60
        deepest = 0
        minutey = 0

        for m2, depth in reversed(list(cumulative_sleep)):
            if m2 < m1 and depth > deepest:
                deepest = depth
                minutey = m2
            m1 = m2

        if deepest > longest_sleep:
            longest_sleep = deepest
            guard_id = guard_number
            sleeping_minute = minutey

    return guard_id * sleeping_minute
