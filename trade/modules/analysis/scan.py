# -*- coding: utf-8 -*-

import configparser
import os

import yaml
from binance import Client

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
GROWTH_FROM = settings['trade']['growth_range']['from']
GROWTH_TO = settings['trade']['growth_range']['to']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def scan() -> list:
    # The function returns the current coins with the price to BUSD and the exchange rate
    tickers = client.get_ticker()
    coins = []
    for ticker in tickers:
        growth = float(ticker['priceChangePercent'])
        if ticker.get("symbol").endswith('BUSD') and GROWTH_FROM < growth < GROWTH_TO:
            coins.append(ticker['symbol'])
    return coins
