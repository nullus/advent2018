# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import Dict, Set, List, Tuple
from collections import defaultdict


def _parse(instructions_text: str) -> Tuple[Set[str], Dict[str, List[str]]]:
    dependencies: Dict[str, List[str]] = defaultdict(list)
    steps: Set[str] = set()

    for line in instructions_text.strip().splitlines():
        dependency, step = line[5], line[36]
        steps.add(step)
        steps.add(dependency)
        dependencies[step].append(dependency)

    return steps, dependencies


def _common(instructions_text: str, parallelism: int, ticks_offset: int) -> Tuple[int, str]:
    steps_remaining, dependencies = _parse(instructions_text)

    worker_assignment: List[Tuple[str, int]] = []
    ticks, order = 0, ""
    while steps_remaining or worker_assignment:
        # Assign jobs
        while len(worker_assignment) < parallelism:
            try:
                step = min(step for step in steps_remaining if step not in dependencies or not dependencies[step])
            except ValueError:
                break
            steps_remaining.remove(step)
            worker_assignment.append((step, ticks + ticks_offset + ord(step) - 64))

        # Find next finishing tasks
        ticks = min(job[1] for job in worker_assignment)
        for finishing_task in sorted([job for job in worker_assignment if job[1] <= ticks], key=lambda k: k[0]):
            order += finishing_task[0]
            worker_assignment.remove(finishing_task)
            dependencies = dict((k, [i for i in v if i != finishing_task[0]]) for k, v in dependencies.items())

    return ticks, order


def part1(instructions_text: str) -> str:
    return _common(instructions_text, 1, 0)[1]


def part2(instructions_text: str, workers: int = 5, base_time: int = 60) -> int:
    return _common(instructions_text, workers, base_time)[0]
