# -*- coding: utf-8 -*-

import os
from decimal import Decimal

import yaml

from modules.analysis.utils import percent_difference

with open('{0}/../../settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

FALL_PERCENTAGE = settings['trade']['sell']['fall_percentage']


def relevance(exchange_rate: Decimal = None, highest_price: Decimal = None) -> bool:
    # Returns True if the coin is still active, else False
    if percent_difference(highest_price, exchange_rate) > FALL_PERCENTAGE:
        # If the difference is greater than N%, then the coin is sold
        return True
    return False
