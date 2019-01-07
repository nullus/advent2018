# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

import re
from itertools import count
from typing import List, Tuple


def parser(particles_text: str) -> List[Tuple[Tuple[int, ...], ...]]:
    return [
        tuple(
            tuple(int(i) for i in part.split(", "))
            for part in re.findall(r'<([^>]+)>', line)
        )
        for line in particles_text.strip().splitlines()
    ]


def _bounds(particles: List[Tuple[Tuple[int, ...], ...]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    return (
        min(particles, key=lambda k: k[0][0])[0][0],
        min(particles, key=lambda k: k[0][1])[0][1]
    ), (
        max(particles, key=lambda k: k[0][0])[0][0],
        max(particles, key=lambda k: k[0][1])[0][1]
    )


def part1(particles_text: str) -> Tuple[int, str]:

    particles = parser(particles_text)
    particles_bounds = _bounds(particles)

    seconds: int = 0
    for seconds in count():
        # Run simulation
        particles_new = [
            ((p[0][0] + p[1][0], p[0][1] + p[1][1]), (p[1][0], p[1][1]))
            for p in particles
        ]
        particles_bounds_new = _bounds(particles_new)
        if (particles_bounds[0][0] >= particles_bounds_new[0][0] and
                particles_bounds[0][1] >= particles_bounds_new[0][1] and
                particles_bounds[1][0] <= particles_bounds_new[1][0] and
                particles_bounds[1][1] <= particles_bounds_new[1][1]):
            break
        particles = particles_new
        particles_bounds = particles_bounds_new

    result = ""

    positions = [i[0] for i in particles]

    for y in range(particles_bounds[0][1], particles_bounds[1][1] + 1):
        for x in range(particles_bounds[0][0], particles_bounds[1][0] + 1):
            if (x, y) in positions:
                result += "#"
            else:
                result += "."
        result += "\n"

    return seconds, result
