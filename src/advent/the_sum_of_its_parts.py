# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import Dict, Set, List, Tuple
from collections import defaultdict


def part1(instructions_text: str) -> str:
    depends: Dict[str, List[str]] = defaultdict(list)
    steps: Set[str] = set()

    for line in instructions_text.strip().splitlines():
        steps.add(line[5])
        steps.add(line[36])
        depends[line[36]].append(line[5])

    order = ""
    while steps:
        next_step = min(step for step in steps if step not in depends or not depends[step])
        steps.remove(next_step)
        depends = dict((k, [i for i in v if i != next_step]) for k, v in depends.items())
        order += next_step

    return order


def part2(instructions_text: str, workers: int = 5, base_time: int = 60) -> int:
    depends: Dict[str, List[str]] = defaultdict(list)
    steps: Set[str] = set()

    for line in instructions_text.strip().splitlines():
        steps.add(line[5])
        steps.add(line[36])
        depends[line[36]].append(line[5])

    worker_assignment: List[Tuple[str, int]] = []
    order = ""
    current_time = 0
    while steps or worker_assignment:
        # Assign jobs
        while len(worker_assignment) < workers:
            try:
                next_step = min(step for step in steps if step not in depends or not depends[step])
            except ValueError:
                break
            steps.remove(next_step)
            worker_assignment.append((next_step, current_time + base_time + ord(next_step) - 64))

        # Find next finishing tasks
        current_time = min(job[1] for job in worker_assignment)
        for finishing_task in sorted([job for job in worker_assignment if job[1] <= current_time], key=lambda k: k[0]):
            order += finishing_task[0]
            worker_assignment.remove(finishing_task)
            depends = dict((k, [i for i in v if i != finishing_task[0]]) for k, v in depends.items())

    return current_time
