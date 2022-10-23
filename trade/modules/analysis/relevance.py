# -*- coding: utf-8 -*-

import configparser
import os
from decimal import Decimal

import yaml
from binance import Client

from trade.modules.analysis.utils import percent_difference
from trade.modules.database import get
from typing import Union

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
FALL_PERCENTAGE = settings['trade']['sell']['fall_percentage']
FALL_PERCENTAGE_TO_BUY = settings['trade']['buy']['fall_percentage']
DEFAULT_PAIR = settings['trade']['default_pair']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def get_highest_price(symbol: str = DEFAULT_PAIR, deal_time: Union[int, float] = None) -> Decimal:
    try:
        deal_time = int(deal_time)
        candles = client.get_klines(
            symbol=symbol,
            interval=client.KLINE_INTERVAL_3MINUTE,
            limit=1000,
            startTime=deal_time * 1000
        )
        rates = [candle[2] for candle in candles]
        highest_price = Decimal(max(rates))
        return highest_price
    except TypeError:
        print('deal time is None')


def relevance(symbol: str = DEFAULT_PAIR, deal_id: int = None) -> bool:
    # Returns True if the coin is still active, else False
    exchange_rate = Decimal(
        client.get_symbol_ticker(symbol=symbol).get('price')
    )
    deal_time = get.deal_time(deal_id)
    highest_price = get_highest_price(symbol, deal_time)
    if percent_difference(highest_price, exchange_rate) > FALL_PERCENTAGE:
        # If the difference is greater than N%, then the coin is sold
        return True
    return False
