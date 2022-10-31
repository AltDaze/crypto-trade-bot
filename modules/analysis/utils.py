# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Union


def percent_difference(first: Union[int, float, Decimal],
                       second: Union[int, float, Decimal]) -> Decimal:
    if first < second:
        first, second = second, first
    difference: Decimal = Decimal(
        (first / second - 1) * 100
    )
    return difference
