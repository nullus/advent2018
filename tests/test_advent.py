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


from pytest import mark

from advent import day_1_1, day_1_2, day_2_1_count, day_2_1, day_2_2, day_2_2_common_elements

test_day_1_1_data = [
    ["+1 +1 +1", 3],
    ["+1 +1 -2", 0],
    ["-1 -2 -3", -6],
]


@mark.parametrize("adjustment, frequency", test_day_1_1_data)
def test_day_1_1(adjustment, frequency):
    assert day_1_1(adjustment) == frequency


test_day_1_2_data = [
    ["+1 -1", 0],
    ["+3 +3 +4 -2 -4", 10],
    ["-6 +3 +8 +5 -6", 5],
    ["+7 +7 -2 -7 -4", 14],
]


@mark.parametrize("adjustment, frequency", test_day_1_2_data)
def test_day_1_2(adjustment, frequency):
    assert day_1_2(adjustment) == frequency


test_day_2_1_count_data = [
    ["abcdef", (0, 0)],
    ["bababc", (1, 1)],
    ["abbcde", (1, 0)],
    ["abcccd", (0, 1)],
    ["aabcdd", (1, 0)],
    ["abcdee", (1, 0)],
    ["ababab", (0, 1)],
]


@mark.parametrize("box_id, count", test_day_2_1_count_data)
def test_day_2_1_count(box_id, count):
    assert day_2_1_count(box_id) == count


test_day_2_1_data = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""


def test_day_2_1():
    assert day_2_1(test_day_2_1_data) == 12


test_day_2_2_data = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""


def test_day_2_2():
    assert "fgij" == day_2_2(test_day_2_2_data)


test_day_2_2_common_elements_data = [
    ["fguij", "fghij", "fgij"],
    ["abcde", "pqrst", ""],
    ["abcde", "axcye", "ace"],
]


@mark.parametrize("this, that, common", test_day_2_2_common_elements_data)
def test_day_2_2_common_elements(this, that, common):
    assert common == day_2_2_common_elements(this, that)
