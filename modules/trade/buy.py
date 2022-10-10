# -*- coding: utf-8 -*-

import configparser
import traceback
from decimal import Decimal

from binance import Client
from binance.helpers import round_step_size

from ..database import create_database
import modules.database as db
from modules.analysis.purchase_analysis import analysis
from modules.analysis.scan import scan

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
DEFAULT_PAIR = config['settings']['default_pair']
PRICE_TO_BUY = config['settings'].getint('price_to_buy')
COINS_LIMIT = config['settings'].getint('coins_limit')

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def buy(symbol: str = DEFAULT_PAIR, price: float = PRICE_TO_BUY) -> client.order_market_buy:
    try:
        symbol_info = client.get_symbol_info(symbol).get("filters")
        min_notional = symbol_info.get(3).get('minNotional')
        step_size = symbol_info.get(2).get('stepSize')
        rate = client.get_symbol_ticker(symbol=symbol).get('price')
        amount = 1 / Decimal(rate) * price
        qty = round_step_size(quantity=amount, step_size=Decimal(step_size))
        if qty > Decimal(min_notional):
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            db.purchased_coin(symbol, qty, rate)
            print(f'[BUY] {qty=} {type(qty)}')
            return order
    except Exception:
        print(traceback.format_exc())


def buy_process():
    # The process of buying a coin
    try:
        for coin in scan():
            if analysis(coin) and db.coins_limit(COINS_LIMIT) and db.purchased_coin_doesnt_exist(coin):
                buy(symbol=coin, price=PRICE_TO_BUY)
    except Exception:
        print(traceback.format_exc())
