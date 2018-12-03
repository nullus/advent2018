# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from typing import Iterator, Tuple, Set


class Rect(object):
    def __init__(self, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def area(self):
        return self.width * self.height

    def contains(self, x: int, y: int) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def overlap(self, other: 'Rect') -> 'Rect':
        return Rect(max(other.x1, self.x1), max(other.y1, self.y1), min(other.x2, self.x2), min(other.y2, self.y2))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Rect):
            return False
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2

    def __hash__(self) -> int:
        return hash((self.x1, self.y1, self.x2, self.y2))

    def __repr__(self) -> str:
        return f"Rect({self.x1}, {self.y1}, {self.x2}, {self.y2})"


class Claim(object):
    def __init__(self, id_: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__()
        self.r = Rect(x, y, x + width, y + height)
        self.id = id_

    def overlap(self, other) -> Rect:
        return self.r.overlap(other.r)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Claim):
            return False
        return self.id == o.id and self.r == o.r

    def __hash__(self) -> int:
        return hash((self.id, hash(self.r)))

    def __repr__(self) -> str:
        return f"Claim({self.id}, {self.r})"


def parse_claims_text(claims_text: str) -> Iterator[Claim]:
    """
    Crude parsing for records like:

    #10 @ 406,555: 11x25
    """
    for line in claims_text.strip().splitlines():
        claim_id, _, offset, size = line.split()
        offset_x, offset_y = offset.strip(':').split(',')
        width, height = size.split('x')
        yield Claim(claim_id, int(offset_x), int(offset_y), int(width), int(height))


def _generate_y_events(claims: Iterator[Claim]) -> Iterator[Tuple[int, Claim]]:
    for claim in claims:
        yield claim.r.y1, claim
        yield claim.r.y2, claim


def _generate_x_events(claims: Iterator[Claim]) -> Iterator[Tuple[int, Claim]]:
    for claim in claims:
        yield claim.r.x1, claim
        yield claim.r.x2, claim


def _scan_claims(claims: Iterator[Claim]) -> Iterator[Tuple[Set[Claim], Rect]]:
    scan_y = set()
    y_events = sorted(_generate_y_events(claims), key=lambda x: x[0])
    y1 = 0
    for y_event in y_events:
        y2, y_claim = y_event
        if y2 > y1:
            scan_x = set()
            x_events = sorted(_generate_x_events(iter(scan_y)), key=lambda x: x[0])
            x1 = 0
            for x_event in x_events:
                x2, x_claim = x_event
                if x2 > x1:
                    yield scan_x, Rect(x1, y1, x2, y2)
                x1 = x2
                scan_x.remove(x_claim) if x_claim in scan_x else scan_x.add(x_claim)
        y1 = y2
        scan_y.remove(y_claim) if y_claim in scan_y else scan_y.add(y_claim)


def part1(claims_text: str) -> int:
    return sum(rect.area for claims, rect in _scan_claims(parse_claims_text(claims_text)) if len(claims) > 1)


def part2(claims_text: str) -> str:
    claims = list(parse_claims_text(claims_text))
    valid_claims = set(claim.id for claim in claims) - set(
        claim.id
        for match_claims, _ in _scan_claims(claims)
        for claim in match_claims
        if len(match_claims) > 1
    )
    return ' '.join(valid_claims)
