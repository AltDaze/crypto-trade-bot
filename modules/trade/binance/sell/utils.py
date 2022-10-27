# -*- coding: utf-8 -*-

import configparser
import os
import traceback
from configparser import ConfigParser
from decimal import Decimal

from binance import Client

from modules.analysis.relevance import relevance
from modules.database import get

config: ConfigParser = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']

client: Client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def get_relevance(coin):
    try:
        deal_id: int = 0
        deal_time: int = get.deal_time(deal_id)
        exchange_rate: Decimal = Decimal(
            client.get_symbol_ticker(symbol=coin).get('price')
        )
        candles: dict = client.get_klines(
            symbol=coin,
            interval=client.KLINE_INTERVAL_3MINUTE,
            limit=1000,
            startTime=deal_time * 1000
        )
        highest_price: Decimal = Decimal(max([candle[2] for candle in candles]))
        return relevance(exchange_rate=exchange_rate, highest_price=highest_price)
    finally:
        print(traceback.format_exc())
        return False
