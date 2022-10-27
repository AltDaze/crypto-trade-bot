# -*- coding: utf-8 -*-

import configparser
import os
from configparser import ConfigParser

from binance import Client

config: ConfigParser = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']

client: Client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def get_prices(coin: str = None) -> tuple:
    candles: dict = client.get_klines(
        symbol=coin,
        interval=client.KLINE_INTERVAL_3MINUTE,
        limit=500
    )
    prices: tuple = tuple([candle[2] for candle in candles])
    return prices
