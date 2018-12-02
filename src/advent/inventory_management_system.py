# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import Counter
from typing import Tuple


def is_letter_repeated_2_3_times(box_id: str) -> Tuple[int, int]:
    return int(any(i == 2 for i in Counter(box_id).values())), int(any(i == 3 for i in Counter(box_id).values()))


def part1(box_ids: str) -> int:
    total_count = (0, 0)
    for box_id in box_ids.split():
        count = is_letter_repeated_2_3_times(box_id)
        total_count = total_count[0] + count[0], total_count[1] + count[1]
    return total_count[0] * total_count[1]


def common_characters(this: str, that: str) -> str:
    return ''.join(i for i, j in zip(this, that) if i == j)


def part2(box_ids_text: str) -> str:
    box_ids = box_ids_text.split()
    matching_id = next(
        common_characters(x, y)
        for i, x in enumerate(box_ids[:-1])
        for y in box_ids[i+1:]
        if len(common_characters(x, y)) == len(x) - 1
    )
    return matching_id
