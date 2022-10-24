# -*- coding: utf-8 -*-

import configparser
import os
import traceback
from configparser import ConfigParser
from decimal import Decimal

import yaml
from binance import Client
from binance.helpers import round_step_size

from modules.analysis.relevance import relevance
from modules.database import get, delete

config: ConfigParser = configparser.ConfigParser()
config.read('{0}/../../config.ini'.format(os.path.dirname(__file__)))

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']
DEFAULT_PAIR = settings['trade']['default_pair']
PRICE_TO_BUY = settings['trade']['price_to_buy']

client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


def sell(symbol: str = DEFAULT_PAIR) -> client.order_market_sell:
    # TODO: Продавать через BNB и в таком случае не надо учитывать комиссию
    try:
        balance = Decimal(client.get_asset_balance(symbol.replace('BUSD', '')).get("free"))
        step_size = Decimal(client.get_symbol_info(symbol).get("filters").get(2).get("stepSize"))
        qty = round_step_size(quantity=balance, step_size=step_size)
        if qty <= balance:
            delete.purchased_coin(symbol)
            return client.order_market_sell(symbol=symbol, quantity=qty)
    finally:
        print(traceback.format_exc())


def sell_all():
    coins = get.the_names_of_purchased_coins()
    if coins is not None:
        for coin in coins:
            sell(coin)


def sell_process():
    try:
        """
        deal_ids = get.all_deal_id()
        for deal_id in deal_ids: ...
        """
        coins = get.the_names_of_purchased_coins()
        if coins is not None:
            for coin in coins:
                if relevance(coin):
                    sell(coin)
    finally:
        print(traceback.format_exc())
