# -*- coding: utf-8 -*-

import decimal
import configparser
# import database as db
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


def sell(symbol: str = DEFAULT_PAIR) -> client.order_market_sell:
    # TODO: Попробовать упростить
    #  заменить все проблемы с lot size на ту цену, которая имеется
    #  учитывать комиссия
    try:
        balance = decimal.Decimal(client.get_asset_balance(symbol.replace('BUSD', ''))['free'])
        symbol_info = client.get_symbol_info(symbol)
        min_notional = decimal.Decimal(symbol_info['filters'][3]['minNotional'])
        step_size = symbol_info['filters'][2]['stepSize']

        # fix lot size
        length = 2
        for i in step_size:
            if i == '1':
                break
            else:
                length += 1

        qty = int(balance) if length == 0 else decimal.Decimal(str(balance)[:length])
        if min_notional <= qty <= balance:
            order = client.order_market_sell(symbol=symbol, quantity=qty)
            # db.remove_purchased_coin(symbol)
            print(f'[SELL] {symbol=} {qty=}')
            return order
    except Exception:
        print(traceback.format_exc())


def sell_all():
    pass
    # coins = db.get_the_names_of_purchased_coins()
    # for coin in coins:
    #     sell(coin)
