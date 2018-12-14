# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import takewhile, dropwhile

from typing import List, Iterator, Tuple


def _gen_score_sequence(initial_scores: List[int]) -> Iterator[int]:
    scores: List[int] = initial_scores.copy()
    len_scores: int = len(scores)
    i, j = 0, 1

    for x in scores:
        yield x

    while True:
        score = scores[i] + scores[j]
        if score > 9:
            yield 1
            yield score % 10
            scores += [1, score % 10]
            len_scores += 2
        else:
            yield score
            scores.append(score)
            len_scores += 1
        i, j = (scores[i] + i + 1) % len_scores, (scores[j] + j + 1) % len_scores


def part1(initial_scores: List[int], attempted_recipes: int) -> str:
    sequence: Iterator[Tuple[int, int]] = takewhile(
        lambda n: n[0] < attempted_recipes + 10,
        dropwhile(
            lambda n: n[0] < attempted_recipes,
            enumerate(_gen_score_sequence(initial_scores))
        )
    )
    return ''.join(str(i[1]) for i in sequence)


def part2(initial_scores: List[int], match_sequence_str: str) -> int:
    match_sequence: List[int] = [int(i) for i in match_sequence_str]
    matched: int = 0

    for i, score in enumerate(_gen_score_sequence(initial_scores)):
        if score == match_sequence[matched]:
            matched += 1
            if matched >= len(match_sequence_str):
                return i - len(match_sequence_str) + 1
        elif score == match_sequence[0]:
            matched = 1
        else:
            matched = 0
