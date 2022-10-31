# -*- coding: utf-8 -*-

from decimal import Decimal

from config import Settings
from modules.analysis.utils import percent_difference
from typing import Final

SELL_FALL_PERCENTAGE: Final = Settings.SELL_FALL_PERCENTAGE


def relevance(exchange_rate: Decimal, highest_price: Decimal) -> bool:
    # Returns True if the coin is still active, else False
    if percent_difference(highest_price, exchange_rate) > SELL_FALL_PERCENTAGE:
        # If the difference is greater than N%, then the coin is sold
        return True
    return False
