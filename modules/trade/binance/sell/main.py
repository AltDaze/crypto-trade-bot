# -*- coding: utf-8 -*-

import os
import traceback
from decimal import Decimal

import yaml
from binance import Client
from binance.helpers import round_step_size

from modules.database.methods import get, delete
from .utils import get_relevance

with open('{0}/../../../../settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

DEFAULT_PAIR = settings['trade']['default_pair']
PRICE_TO_BUY = settings['trade']['price_to_buy']


def sell(client: Client, symbol: str) -> Client.order_market_sell:
    # TODO: Продавать через BNB и в таком случае не надо учитывать комиссию
    try:
        balance: Decimal = Decimal(
            client.get_asset_balance(symbol.replace('BUSD', '')).get("free")
        )
        step_size: Decimal = Decimal(
            client.get_symbol_info(symbol).get("filters").get(2).get("stepSize")
        )
        qty: float = round_step_size(quantity=balance, step_size=step_size)
        if qty <= balance:
            delete.purchased_coin(symbol)
            return client.order_market_sell(symbol=symbol, quantity=qty)
    finally:
        print(traceback.format_exc())


def sell_all(client: Client) -> None:
    coins = get.the_names_of_purchased_coins()
    if coins is not None:
        for coin in coins:
            sell(client=client, symbol=coin)


def sell_process(client: Client) -> None:
    try:
        """
        deal_ids = get.all_deal_id()
        for deal_id in deal_ids: ...
        """
        # TODO: Change coins =get.the_names... на deal_ids = get.all_deal...
        coins: list = get.the_names_of_purchased_coins()
        if coins is not None:
            for coin in coins:
                if get_relevance(client=client, coin=coin):
                    sell(client=client, symbol=coin)
    finally:
        print(traceback.format_exc())
