# -*- coding: utf-8 -*-

import configparser
from decimal import Decimal
from .utils import percent_difference
from binance import Client
from modules.database import update, get


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
FALL_PERCENTAGE = config['settings'].getfloat('fall_percentage')
FALL_PERCENTAGE_TO_BUY = config['settings'].getfloat('fall_percentage_to_buy')
DEFAULT_PAIR = config['settings']['default_pair']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def relevance(symbol: str = DEFAULT_PAIR) -> bool:
    # Returns True if the coin is still active, else False
    # TODO: REMAKE
    exchange_rate = Decimal(client.get_symbol_ticker(symbol=symbol)['price'])
    update.historically_highest_coin_value(symbol, exchange_rate)
    highest_price = get.historically_highest_coin_price(symbol)
    if percent_difference(highest_price, exchange_rate) > FALL_PERCENTAGE:
        # If the difference is greater than N%, then the coin is sold
        return True
    return False