# -*- coding: utf-8 -*-

import configparser
import pprint
import traceback
from decimal import Decimal

import binance.exceptions
from binance import Client
from binance.helpers import round_step_size

# from ..database import create_database
import modules.database.database as db
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
        min_notional = symbol_info[3].get('minNotional')
        step_size = symbol_info[2].get('stepSize')
        rate = client.get_symbol_ticker(symbol=symbol).get('price')
        amount = 1 / Decimal(rate) * price
        qty = round_step_size(quantity=amount, step_size=Decimal(step_size))
        if qty > Decimal(min_notional):
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            db.purchased_coin(symbol, qty, rate)
            print(f'[BUY] {symbol=} {qty=} {type(qty)}')
            return order
    except binance.exceptions.BinanceAPIException as ex:
        match ex.code:
            case -1013:
                pass
            case -2010:
                raise SystemExit(f'{ex.code=} ({ex.message=})')
    finally:
        print(traceback.format_exc())


def buy_process():
    for coin in scan():
        if analysis(coin) and db.coins_limit(COINS_LIMIT) and db.purchased_coin_doesnt_exist(coin):
            buy(symbol=coin, price=PRICE_TO_BUY)
