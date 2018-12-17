# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from collections import defaultdict
from typing import Any, Set, Dict


def _exec(reg, loc, res):
    next_reg = reg.copy()
    next_reg[loc] = res
    return next_reg


_opcodes = {
    'addr': lambda reg, a, b, c: _exec(reg, c, reg[a] + reg[b]),
    'addi': lambda reg, a, b, c: _exec(reg, c, reg[a] + b),
    'mulr': lambda reg, a, b, c: _exec(reg, c, reg[a] * reg[b]),
    'muli': lambda reg, a, b, c: _exec(reg, c, reg[a] * b),
    'banr': lambda reg, a, b, c: _exec(reg, c, reg[a] & reg[b]),
    'bani': lambda reg, a, b, c: _exec(reg, c, reg[a] & b),
    'borr': lambda reg, a, b, c: _exec(reg, c, reg[a] | reg[b]),
    'bori': lambda reg, a, b, c: _exec(reg, c, reg[a] | b),
    'setr': lambda reg, a, b, c: _exec(reg, c, reg[a]),
    'seti': lambda reg, a, b, c: _exec(reg, c, a),
    'gtir': lambda reg, a, b, c: _exec(reg, c, int(a > reg[b])),
    'gtri': lambda reg, a, b, c: _exec(reg, c, int(reg[a] > b)),
    'gtrr': lambda reg, a, b, c: _exec(reg, c, int(reg[a] > reg[b])),
    'eqir': lambda reg, a, b, c: _exec(reg, c, int(a == reg[b])),
    'eqri': lambda reg, a, b, c: _exec(reg, c, int(reg[a] == b)),
    'eqrr': lambda reg, a, b, c: _exec(reg, c, int(reg[a] == reg[b])),
}


def part1(sample_text: str) -> Any:
    three_options_or_more: int = 0
    reg, exp, ins = None, None, None

    # Skip blank lines
    for line in filter(None, sample_text.splitlines()):
        if line.startswith('Before: '):
            reg = [int(i) for i in line[8:].strip('[]').split(', ')]
        elif line.startswith('After:  '):
            exp = [int(i) for i in line[8:].strip('[]').split(', ')]
            # Test instruction
            if [run(reg, *ins[1:]) == exp for run in _opcodes.values()].count(True) >= 3:
                three_options_or_more += 1
        else:
            ins = [int(i) for i in line.split()]

    return three_options_or_more


def part2(sample_text: str, program_text: str) -> int:
    reg, exp, ins = None, None, None
    opcode_candidate: Dict[int, Set[str]] = defaultdict(lambda: set(_opcodes.keys()))
    opcode_mapping: Dict[int, str] = defaultdict(lambda: '')

    # Skip blank lines
    for line in filter(None, sample_text.splitlines()):
        if line.startswith('Before: '):
            reg = [int(i) for i in line[8:].strip('[]').split(', ')]
        elif line.startswith('After:  '):
            exp = [int(i) for i in line[8:].strip('[]').split(', ')]
            # Test instruction
            opcode_candidate[ins[0]].intersection_update(
                [opcode for opcode, run in _opcodes.items() if run(reg, *ins[1:]) == exp]
            )
        else:
            ins = [int(i) for i in line.split()]

    # Reduce the candidate selection based on mappings we're certain of
    while opcode_candidate:
        # Transfer opcodes with a single candidate
        opcode_mapping.update({v: k.pop() for v, k in opcode_candidate.items() if len(k) == 1})
        # Remove opcodes from the mapping table, skipping over empty sets
        opcode_candidate = {v: k.difference(opcode_mapping.values()) for v, k in opcode_candidate.items() if k}

    reg = [0, 0, 0, 0]
    for line in program_text.splitlines():
        ins = [int(i) for i in line.split()]
        reg = _opcodes[opcode_mapping[ins[0]]](reg, *ins[1:])

    return reg[0]
