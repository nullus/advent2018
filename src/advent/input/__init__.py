# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from importlib.resources import read_text


def text(input_name: str):
    return read_text(__name__, input_name)
