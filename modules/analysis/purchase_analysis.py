# -*- coding: utf-8 -*-

import configparser
import os
from configparser import ConfigParser

import yaml
from binance import Client

from .utils import percent_difference

config: ConfigParser = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
FALL_PERCENTAGE_TO_BUY = settings['trade']['buy']['fall_percentage']
DEFAULT_PAIR = settings['trade']['default_pair']

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
    prices = [candle[2] for candle in candles]
    highest_price = float(max(prices))
    lowest_price = float(min(prices))
    # TODO: Попытаться реализовать градацию роста за последнее время, - дополнительный фактор при анализе
    if lowest_price < current_price and percent_difference(highest_price, lowest_price) < FALL_PERCENTAGE_TO_BUY:
        return True
    return False
