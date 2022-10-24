# -*- coding: utf-8 -*-

import configparser
import os
import traceback
from configparser import ConfigParser
from decimal import Decimal
from pprint import pprint as pp
from typing import Union

import binance.exceptions
import yaml
from binance import Client
from binance.helpers import round_step_size

from modules.analysis.purchase_analysis import analysis
from modules.analysis.scan import scan
from modules.database import get, create


config: ConfigParser = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

with open('{0}/../../settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
DEFAULT_PAIR = settings['trade']['default_pair']
PRICE_TO_BUY = settings['trade']['price_to_buy']
COINS_LIMIT = settings['trade']['coins_limit']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def buy(symbol: str = DEFAULT_PAIR, price: Union[float, Decimal] = PRICE_TO_BUY) -> client.order_market_buy:
    try:
        symbol_info = client.get_symbol_info(symbol).get("filters")
        min_notional = Decimal(
            symbol_info[3].get('minNotional')
        )
        step_size = Decimal(
            symbol_info[2].get('stepSize')
        )
        rate = Decimal(
            client.get_symbol_ticker(symbol=symbol).get('price')
        )
        amount = 1 / rate * price
        qty = round_step_size(quantity=amount, step_size=step_size)
        if qty > min_notional:
            #  TODO: logs in postgresql
            client.order_market_buy(symbol=symbol, quantity=qty)
            create.purchased_coin(symbol, qty, rate)
    except binance.exceptions.BinanceAPIException as ex:
        match ex.code:
            case -1013:  # Filter failure: MIN_NOTIONAL
                print(f'Error: {ex.code=} ({ex.message=})')
            case -2010:  # Account is empty
                print(f'Error: {ex.code=} ({ex.message=})')
                # raise SystemExit(f'{ex.code=} ({ex.message=})')
            case _:
                print(f'Error: {ex.code=} ({ex.message=})')
    finally:
        print(traceback.format_exc())


def buy_process():
    coins = scan()
    pp(coins)
    for coin in coins:
        if analysis(coin) and get.coins_limit(COINS_LIMIT) and get.purchased_coin_doesnt_exist(coin):
            buy(symbol=coin, price=PRICE_TO_BUY)
