# -*- coding: utf-8 -*-

import configparser
import os
from decimal import Decimal

import yaml
from binance import Client

config = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

with open("{0}/../../settings.yaml".format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
GROWTH_FROM = settings['trade']['growth_range']['from']
GROWTH_TO = settings['trade']['growth_range']['to']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def scan() -> tuple:
    # The function returns the current coins with the price to BUSD and the exchange rate
    tickers = client.get_ticker()
    pairs = []
    for ticker in tickers:
        growth = Decimal(ticker['priceChangePercent'])
        symbol = ticker.get("symbol")
        if symbol.endswith('BUSD') and GROWTH_FROM < growth < GROWTH_TO:
            pairs.append(symbol)
    return tuple(pairs)
