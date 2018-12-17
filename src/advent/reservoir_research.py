# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import count
from operator import sub
from typing import List, Tuple


def generate_map(scan_locations: str) -> Tuple[Tuple[int, int], List[List[str]]]:

    vert_seam = []
    horiz_seam = []

    # Start bounds around spring
    x_min, x_max, y_min, y_max = 500, 500, 0, 0

    for line in scan_locations.splitlines():
        pos, range_ = line.split(", ")
        pos_axis, pos_value = pos.split("=")
        range_axis, range_value = range_.split("=")
        range_value = range_value.split("..")

        if pos_axis == 'x':
            x, y1, y2 = int(pos_value), int(range_value[0]), int(range_value[1])
            x_min = min(x, x_min)
            x_max = max(x, x_max)
            y_min = min(y1, y_min)
            y_max = max(y2, y_max)

            vert_seam.append((x, range(y1, y2+1)))
        elif pos_axis == 'y':
            y, x1, x2 = int(pos_value), int(range_value[0]), int(range_value[1])
            x_min = min(x1, x_min)
            x_max = max(x2, x_max)
            y_min = min(y, y_min)
            y_max = max(y, y_max)

            horiz_seam.append((y, range(x1, x2+1)))

    # Generate map around min/max coordinates
    offset = x_min - 1, y_min

    map_ = []
    for y in range(y_min, y_max + 1):
        # Add a buffer around seams
        line = []

        for x in range(x_min - 1, x_max + 2):
            if (x, y) == (500, 0):
                # Spring
                line.append('+')
            elif any(y == h[0] and x in h[1] for h in horiz_seam):
                # Clay
                line.append('#')
            elif any(x == v[0] and y in v[1] for v in vert_seam):
                # Clay
                line.append('#')
            else:
                # Sand
                line.append('.')
        map_.append(line)

    return offset, map_


def part1(scan_locations: str) -> int:
    offset, map_ = generate_map(scan_locations)

    def _scan_and_fill_horiz(location):
        next_scan_and_fill = []

        y = location[1]

        if y >= len(map_) - 1:
            return None

        # scan left and right
        x1 = location[0]
        for x1 in count(location[0], -1):
            if map_[y + 1][x1] not in ('#', '~'):
                # fall through
                next_scan_and_fill.append((x1, y))
                break
            elif map_[y][x1 - 1] in ('#', '~'):
                break

        x2 = location[0]
        for x2 in count(location[0]):
            if map_[y + 1][x2] not in ('#', '~'):
                # fall through
                next_scan_and_fill.append((x2, y))
                break
            elif map_[y][x2 + 1] in ('#', '~'):
                break

        if not next_scan_and_fill:
            for u in range(x1, x2 + 1):
                map_[y][u] = '~'
            return location[0], y - 1
        else:
            for u in range(x1, x2 + 1):
                map_[y][u] = '|'
            while next_scan_and_fill:
                _scan_and_fill(next_scan_and_fill.pop())

        return None

    def _scan_and_fill(location):
        y = location[1]
        try:
            for y in count(location[1]):
                if map_[y + 1][location[0]] in ('#', '~'):
                    break
        except IndexError:
            # We ran out of map!
            y += 1

        # Draw the "|"
        for v in range(location[1] + 1, y):
            map_[v][location[0]] = '|'

        last_location = _scan_and_fill_horiz((location[0], y))

        if last_location:
            _scan_and_fill(last_location)

    _scan_and_fill(tuple(map(sub, (500, 0), offset)))

    print()
    print('\n'.join(''.join(row) for row in map_))

    return sum(row.count('~') + row.count('|') for row in map_)
