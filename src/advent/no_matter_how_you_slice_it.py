# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.
from itertools import chain
from typing import Iterator, List, Optional


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


class Claim(object):
    def __init__(self, id_: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__()
        self.r = Rect(x, x + width, y, y + height)
        self.id = id_

    def overlap(self, other) -> Rect:
        return self.r.overlap(other.r)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Claim):
            return False
        return self.id == o.id and self.r == o.r


def claims(claims_text: str) -> Iterator[Claim]:
    """
    Crude parsing for records like:

    #10 @ 406,555: 11x25
    """
    for line in claims_text.splitlines():
        claim_id, _, offset, size = line.split()
        offset_x, offset_y = offset.strip(':').split(',')
        width, height = size.split('x')
        yield Claim(claim_id, int(offset_x), int(offset_y), int(width), int(height))


class QNode(object):
    def __init__(self, bounds: Rect) -> None:
        super().__init__()
        self.child: Optional[List[QNode]] = None
        self.bounds = bounds

    def split(self, x: int, y: int):
        self.child = [
            QNode(Rect(self.bounds.x1, self.bounds.y1, x, y)),
            QNode(Rect(x, self.bounds.y1, self.bounds.x2, y)),
            QNode(Rect(x, y, self.bounds.x2, self.bounds.y2)),
            QNode(Rect(self.bounds.x1, y, x, self.bounds.y2)),
        ]


class QTree(object):
    def __init__(self, width, height) -> None:
        super().__init__()
        self.root = QNode(Rect(0, 0, width, height))

    def _qnodes(self, qnode: QNode) -> Iterator[QNode]:
        if qnode.child:
            return chain(
                self._qnodes(qnode.child[0]),
                self._qnodes(qnode.child[1]),
                self._qnodes(qnode.child[2]),
                self._qnodes(qnode.child[3]),
            )
        else:
            yield qnode

    def __iter__(self) -> Iterator[Rect]:
        for i in self._qnodes(self.root):
            yield i.bounds

    def insert(self, param: Rect):
        pass


def part1(claims_text: str) -> int:
    pass
