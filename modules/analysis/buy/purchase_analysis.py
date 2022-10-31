# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Final

from config import Settings
from modules.analysis.utils import percent_difference

BUY_FALL_PERCENTAGE: Final = Settings.BUY_FALL_PERCENTAGE


def analysis(prices: tuple, current_price: Decimal) -> bool:
    # Analysis for buying a coin
    # The fact that it is still rising and not falling
    highest_price: float = float(max(prices))
    lowest_price: float = float(min(prices))
    # TODO: Попытаться реализовать градацию роста за последнее время, - дополнительный фактор при анализе
    if lowest_price < current_price and \
            percent_difference(highest_price, lowest_price) < BUY_FALL_PERCENTAGE:
        return True
    return False
