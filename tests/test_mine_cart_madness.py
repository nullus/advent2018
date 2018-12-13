# coding: utf-8
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>. All rights reserved.
# Licensed under BSD 2-Clause License. See LICENSE file for full license.

from pytest import mark

from advent.mine_cart_madness import part1, Cart, part2

test_data = '''
/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   
'''.strip()


def test_part1():
    assert (7, 3) == part1(test_data)


def test_cart_turn():
    cart = Cart((0, 0), '<')
    cart.turn()
    assert 'v' == cart.direction
    cart.turn()
    assert 'v' == cart.direction
    cart.turn()
    assert '<' == cart.direction


test_cart_order_data = [
    [(1, 1), (0, 0)],
    [(2, 0), (0, 0)],
    [(0, 1), (10, 0)],
]


@mark.parametrize("high_pos, low_pos", test_cart_order_data)
def test_cart_order(high_pos, low_pos):
    cart_low = Cart(low_pos, '>')
    cart_high = Cart(high_pos, '>')

    assert cart_low < cart_high


test_collision_order = '''
/--->--<----\\
|           |
v           v
|           |
|           |
^           ^
|           |
\\->--<------/
'''.strip()


def test_part1_collision_order():
    assert (6, 0) == part1(test_collision_order)


test_data2 = '''
/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
'''.strip()


def test_part2():
    assert (6, 4) == part2(test_data2)
