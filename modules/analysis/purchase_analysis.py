# -*- coding: utf-8 -*-

import configparser
from .utils import percent_difference
from binance import Client


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
FALL_PERCENTAGE_TO_BUY = config['settings'].getfloat('fall_percentage_to_buy')
DEFAULT_PAIR = config['settings']['default_pair']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def analysis(symbol: str = DEFAULT_PAIR) -> bool:
    # Analysis for buying a coin
    # The fact that it is still rising and not falling
    candles = client.get_klines(
        symbol=symbol,
        interval=client.KLINE_INTERVAL_3MINUTE,
        limit=500
        )
    current_price = float(client.get_symbol_ticker(symbol=symbol).get("price"))
    highest_price = current_price
    lowest_price = current_price
    for candle in candles:
        price = float(candle[2])  # High price
        if price > highest_price:
            highest_price = price
        if price < lowest_price:
            lowest_price = price
    if lowest_price < current_price and percent_difference(highest_price, lowest_price) < FALL_PERCENTAGE_TO_BUY:
        return True
    return False
