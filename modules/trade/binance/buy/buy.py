# -*- coding: utf-8 -*-

import configparser
import os
import traceback
from configparser import ConfigParser
from decimal import Decimal
from typing import Optional

import binance.exceptions
import yaml
from binance import Client
from binance.helpers import round_step_size

from modules.analysis.purchase_analysis import analysis
from modules.analysis.scan import scan
from modules.database import get, create
from modules.trade.binance.buy.utils import get_prices

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


def buy(symbol: str = DEFAULT_PAIR, price: Optional[Decimal] = PRICE_TO_BUY) -> client.order_market_buy:
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
    coins: tuple = scan(client.get_ticker())
    for coin in coins:
        current_price: Decimal = Decimal(
            client.get_symbol_ticker(symbol=coin).get('price')
        )
        rising: bool = analysis(
            prices=get_prices(),
            current_price=current_price
        )
        if rising and get.coins_limit(COINS_LIMIT) and get.purchased_coin_doesnt_exist(coin):
            buy(symbol=coin, price=PRICE_TO_BUY)
