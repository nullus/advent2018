# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from more_itertools import take


def part1(license_text: str) -> int:
    numbers = (int(i) for i in license_text.split())

    def process_record(iterable):
        num_child_nodes, num_metadata_entries = next(iterable), next(iterable)
        result = []
        for i in range(num_child_nodes):
            result += process_record(iterable)
        metadata_entries = take(num_metadata_entries, iterable)
        return [metadata_entries] + result

    records = process_record(numbers)
    return sum(sum(i) for i in records)


def part2(license_text: str) -> int:
    numbers = (int(i) for i in license_text.split())

    def process_record(iterable, parent):
        num_child_nodes, num_metadata_entries = next(iterable), next(iterable)
        children = []
        for i in range(num_child_nodes):
            children += process_record(iterable, parent + 1)

        metadata_entries = take(num_metadata_entries, iterable)

        if num_child_nodes:
            direct_children = [i[1] for i in children if i[0] == parent + 1]
            value = sum(direct_children[i-1] for i in metadata_entries if 0 < i <= len(direct_children))
        else:
            value = sum(metadata_entries)

        return [(parent, value, [metadata_entries])] + children

    return process_record(numbers, 0)[0][1]
