# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Union


def percent_difference(first: Union[float, Decimal], second: Union[float, Decimal]) -> Decimal:
    if first < second:
        first, second = second, first
    difference = (first / second - 1) * 100
    return difference
