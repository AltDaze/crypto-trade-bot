# -*- coding: utf-8 -*-

import configparser
from binance import Client


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def scan() -> list:
    # The function returns the current coins with the price to BUSD and the exchange rate
    tickers = client.get_ticker()
    coins = []
    for ticker in tickers:
        change = float(ticker['priceChangePercent'])
        if ticker.get("symbol").endswith('BUSD') and 0 < change < 100:
            coins.append(ticker['symbol'])
    return coins
