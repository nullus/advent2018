# coding: utf-8
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from collections import Counter
from itertools import cycle, accumulate
from typing import Set, Tuple


def day_1_1(adjustments: str) -> int:
    return sum(int(i) for i in adjustments.split())


def day_1_2(adjustments: str) -> int:
    frequencies: Set[int] = {0}
    value = 0
    for i in cycle(adjustments.split()):
        value += int(i)
        if value in frequencies:
            return value
        frequencies.add(value)


def day_2_1_count(box_id: str) -> Tuple[int, int]:
    return int(any(i == 2 for i in Counter(box_id).values())), int(any(i == 3 for i in Counter(box_id).values()))


def day_2_1(box_ids: str) -> int:
    total_count = (0, 0)
    for box_id in box_ids.split():
        count = day_2_1_count(box_id)
        total_count = total_count[0] + count[0], total_count[1] + count[1]
    return total_count[0] * total_count[1]


def day_2_2_common_elements(this: str, that: str) -> str:
    return ''.join(i for i, j in zip(this, that) if i == j)


def day_2_2(box_ids_text: str) -> str:
    box_ids = box_ids_text.split()
    matching_id = next(
        day_2_2_common_elements(x, y)
        for i, x in enumerate(box_ids[:-1])
        for y in box_ids[i+1:]
        if len(day_2_2_common_elements(x, y)) == len(x) - 1
    )
    return matching_id
