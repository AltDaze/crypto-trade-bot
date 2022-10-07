# -*- coding: utf-8 -*-

import configparser

from binance import Client


config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
FALL_PERCENTAGE = config['settings'].getfloat('fall_percentage')
FALL_PERCENTAGE_TO_BUY = config['settings'].getfloat('fall_percentage_to_buy')
DEFAULT_PAIR = config['settings']['default_pair']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def scan() -> list:
    # The function returns the current coins with the price to BUSD and the exchange rate
    tickers = client.get_ticker()
    coins = []
    for ticker in tickers:
        change = float(ticker['priceChangePercent'])
        if ticker.get("symbol").endswith('BUSD') and 10 < change < 100:
            coins.append(ticker['symbol'])
    return coins


# import database as db
#
#
# def detailed_view_of_prices_for_the_last_day(symbol: str) -> client.get_klines:
#     candles = client.get_klines(
#         symbol=symbol,
#         interval=client.KLINE_INTERVAL_1MINUTE
#         )
#     return candles
#
#
# def percent_difference(first: float, second: float) -> float:
#     if first < second:
#         first, second = second, first
#     difference = (first / second - 1) * 100
#     return difference
#
#
# def coin_relevance(symbol: str = DEFAULT_PAIR) -> bool:
#     # Returns True if the coin is still active, else False
#     exchange_rate = float(client.get_symbol_ticker(symbol=symbol)['price'])
#     db.update_historically_highest_coin_value(symbol, exchange_rate)
#     highest_price = db.get_historically_highest_coin_price(symbol)
#     if percent_difference(highest_price, exchange_rate) > FALL_PERCENTAGE:
#         # If the difference is greater than N%, then the coin is sold
#         return True
#     return False
#
#
# def coin_analysis(symbol: str = DEFAULT_PAIR) -> bool:
#     # Analysis for buying a coin
#     # The fact that it is still rising and not falling
#     candles = client.get_klines(
#         symbol=symbol,
#         interval=client.KLINE_INTERVAL_3MINUTE,
#         limit=500
#         )
#     current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
#     highest_price = current_price
#     lowest_price = current_price
#     for candle in candles:
#         price = float(candle[2])  # High price
#         if price > highest_price:
#             highest_price = price
#         if price < lowest_price:
#             lowest_price = price
#     if lowest_price < current_price and percent_difference(highest_price, lowest_price) < FALL_PERCENTAGE_TO_BUY:
#         return True
#     return False
