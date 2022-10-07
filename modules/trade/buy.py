# -*- coding: utf-8 -*-

import decimal
import configparser

from ..database import create_database


import traceback
from binance import Client
from binance.helpers import round_step_size

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
DEFAULT_PAIR = config['settings']['default_pair']
PRICE_TO_BUY = config['settings'].getint('price_to_buy')

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def buy(symbol: str = DEFAULT_PAIR, price: float = PRICE_TO_BUY) -> client.order_market_buy:
    try:
        pass
        # if db.purchased_coin_doesnt_exist(symbol):
        #     symbol_info = client.get_symbol_info(symbol)
        #     min_notional = symbol_info['filters'][3]['minNotional']
        #     step_size = symbol_info['filters'][2]['stepSize']
        #     rate = float(client.get_symbol_ticker(symbol=symbol)['price'])
        #     amount = 1 / rate * price
        #     qty = round_step_size(quantity=amount, step_size=decimal.Decimal(step_size))
        #     if float(qty) > float(min_notional):
        #         order = client.order_market_buy(
        #             symbol=symbol,
        #             quantity=qty,
        #             recvWindow=10 * 1000  # 10 sec / 10000 mlsec
        #         )
        #         db.purchased_coin(symbol, qty, rate)
        #         print(f'[BUY] {qty=} {type(qty)}')
        #         return order
    except Exception:
        print(traceback.format_exc())