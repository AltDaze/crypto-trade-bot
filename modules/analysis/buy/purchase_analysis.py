# -*- coding: utf-8 -*-

import os
from decimal import Decimal

import yaml

from modules.analysis.utils import percent_difference

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

FALL_PERCENTAGE_TO_BUY = settings['trade']['buy']['fall_percentage']


def analysis(prices: tuple, current_price: Decimal) -> bool:
    # Analysis for buying a coin
    # The fact that it is still rising and not falling
    highest_price: float = float(max(prices))
    lowest_price: float = float(min(prices))
    # TODO: Попытаться реализовать градацию роста за последнее время, - дополнительный фактор при анализе
    if lowest_price < current_price and \
            percent_difference(highest_price, lowest_price) < FALL_PERCENTAGE_TO_BUY:
        return True
    return False
