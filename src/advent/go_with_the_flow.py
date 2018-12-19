# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from itertools import dropwhile, chain
from math import sqrt
from typing import List, Tuple, Iterator

from advent.chronal_classification import opcodes


def _execute(ip, text: List[Tuple[str, List[int]]], ip_register: int, registers: List[int]) -> Iterator[List[int]]:
    while ip < len(text):
        opcode, operands = text[ip]
        registers[ip_register] = ip
        registers = opcodes[opcode](registers, *operands)
        yield registers
        ip = registers[ip_register] + 1


def _parse(program_text: str) -> Tuple[List[Tuple[str, List[int]]], int]:
    text = []
    ip_register = None
    for inst in program_text.strip().splitlines():
        opcode, operands = inst.split(maxsplit=1)
        if opcode == '#ip':
            # technically not an opcode
            ip_register = int(operands)
        else:
            text.append((opcode, [int(i) for i in operands.split()]))

    return text, ip_register


def part1(program_text: str) -> int:
    text, ip_register = _parse(program_text)
    registers = [0] * 6
    for registers in _execute(0, text, ip_register, registers):
        # Just burn the iterator
        pass
    return registers[0]


def part2(program_text: str) -> int:
    text, ip_register = _parse(program_text)
    # Run the initialisation
    registers = next(dropwhile(lambda x: x[0] == 1, _execute(0, text, ip_register, [1] + [0] * 5)))
    # Re-implement, more or less (the set is just to avoid the case where register[5] is a perfect square)
    return sum(set(chain.from_iterable(
        (i, int(registers[5] / i))
        for i in range(1, int(sqrt(registers[5])) + 1)
        if not registers[5] % i
    )))


def part2_patch(program_text: str) -> int:
    """
    Speed up the execution by patching the program text, it's not fast, but it _actually_ finishes
    """
    text, ip_register = _parse(program_text)

    # Patch the instructions to speed up execution
    assert text[2] == ('seti', [1, 6, 1])
    assert text[3] == ('mulr', [3, 1, 2])
    assert text[4] == ('eqrr', [2, 5, 2])
    assert text[8] == ('addi', [1, 1, 1])

    text[2] = ('setr', [3, 6, 1])
    # noop
    text[3] = ('seti', [3, 0, 4])
    text[4] = ('eqrr', [1, 5, 2])
    text[8] = ('addr', [1, 3, 1])

    registers = [1] + [0] * 5
    for registers in _execute(0, text, ip_register, registers):
        # Just burn the iterator
        pass
    return registers[0]
