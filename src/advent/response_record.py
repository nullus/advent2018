# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict
from itertools import accumulate
from re import findall
from typing import List, Dict, Tuple, Iterator


def _guard_sleep_journal(response_record_text: str) -> Tuple[Dict[int, int], Dict[int, List[Tuple[int, int]]]]:
    guard_total_sleep: Dict[int, int] = defaultdict(lambda: 0)
    guard_sleep_times: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    guard: int = None

    for record in sorted(response_record_text.strip().splitlines()):
        minutes: int = int(record[15:17])
        action: str = record[19:]

        if action.startswith('Guard'):
            guard = int(action[7:-13])
        elif action.startswith('falls asleep'):
            guard_sleep_times[guard].append((minutes, 1))
        elif action.startswith('wakes up'):
            guard_sleep_times[guard].append((minutes, -1))
            (m1, _), (m2, _) = guard_sleep_times[guard][-2:]
            guard_total_sleep[guard] += m2 - m1
        else:
            raise RuntimeError()

    return guard_total_sleep, guard_sleep_times


def part1(response_record_text: str) -> int:

    guard_total_sleep, guard_sleep_times = _guard_sleep_journal(response_record_text)

    sleepy_guard = sorted(((v, k) for k, v in guard_total_sleep.items()), key=lambda x: x[0], reverse=True)[0][1]

    cumulative_sleep = accumulate(sorted(guard_sleep_times[sleepy_guard], key=lambda x: x[0]),
                                  func=lambda a, b: (b[0], a[1] + b[1]))

    m1 = 60
    deepest = 0
    minutey = 0
    for m2, depth in reversed(list(cumulative_sleep)):
        if m2 < m1 and depth > deepest:
            deepest = depth
            minutey = m2
        m1 = m2

    return minutey * sleepy_guard


def part2(response_record_text: str) -> int:

    guard_total_sleep, guard_sleep_times = _guard_sleep_journal(response_record_text)

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


def impl1(response_record_text: str) -> Iterator[int]:
    """
    Copyright (c) 2018 Peter Tseng (https://github.com/petertseng). All rights reserved.
    Licensed under Apache 2.0 License.
    See https://github.com/petertseng/adventofcode-rb-2018/blob/master/LICENSE for full license.

    Reimplementation of https://github.com/petertseng/adventofcode-rb-2018/blob/master/04_repose_record.rb in Python

    I really liked his solution, but I needed to improve my knowledge of Ruby to comprehend it. This seemed like a good
    way to accomplish that.
    """
    guards = defaultdict(lambda: defaultdict(lambda: 0))

    guard = None
    started_sleeping = None

    for line in sorted(response_record_text.strip().splitlines()):
        last_number = int(findall(r'\d+', line)[-1])
        if line.endswith('begins shift'):
            guard = last_number
        elif line.endswith('falls asleep'):
            started_sleeping = last_number
        elif line.endswith('wakes up'):
            woke_up = last_number
            for min_ in range(started_sleeping, woke_up):
                guards[guard][min_] += 1

    for f in (sum, max):
        id_, minutes = max(guards.items(), key=lambda v: f(v[1].values()))
        yield id_ * max(minutes, key=lambda k: minutes[k])
