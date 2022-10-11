# -*- coding: utf-8 -*-

import configparser
import traceback
from decimal import Decimal
from binance import Client
from binance.helpers import round_step_size
import modules.database.database as db
from modules.analysis.relevance import relevance

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
DEFAULT_PAIR = config['settings']['default_pair']
PRICE_TO_BUY = config['settings'].getint('price_to_buy')

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def sell(symbol: str = DEFAULT_PAIR) -> client.order_market_sell:
    # TODO: Продавать через BNB и в таком случае не надо учитывать комиссию
    try:
        """
        balance = Decimal(client.get_asset_balance(symbol.replace('BUSD', ''))['free'])
        symbol_info = client.get_symbol_info(symbol)
        step_size = symbol_info['filters'][2]['stepSize']

        # fix lot size
        length = 2
        for i in step_size:
            if i == '1':
                break
            else:
                length += 1

        qty = balance if length == 0 else Decimal(str(balance)[:length])  # [:step_size.find("1")-1]
        """
        balance = Decimal(client.get_asset_balance(symbol.replace('BUSD', '')).get("free"))
        step_size = client.get_symbol_info(symbol).get("filters").get(2).get("stepSize")
        qty = round_step_size(quantity=balance, step_size=Decimal(step_size))
        if qty <= balance:
            order = client.order_market_sell(symbol=symbol, quantity=qty)
            db.remove_purchased_coin(symbol)
            print(f'[SELL] {symbol=} {qty=}')
            return order
    except Exception:
        print(traceback.format_exc())


def sell_all():
    pass
    # coins = db.get_the_names_of_purchased_coins()
    # for coin in coins:
    #     sell(coin)


def sell_process():
    # The process of selling a coin
    try:
        coins = db.get_the_names_of_purchased_coins()
        for coin in coins:
            if relevance(coin):
                sell(coin)
    except Exception:
        print(traceback.format_exc())
