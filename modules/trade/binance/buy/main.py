# -*- coding: utf-8 -*-

import os
import traceback
from decimal import Decimal

import binance.exceptions
import yaml
from binance import Client

from modules.analysis.buy.purchase_analysis import analysis
from modules.analysis.buy.scan import scan
from modules.database.methods import get
from modules.trade.binance.buy.utils import get_prices, get_qty, get_min_notional

with open('{0}/../../../../settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

DEFAULT_PAIR = settings['trade']['default_pair']
PRICE_TO_BUY = settings['trade']['price_to_buy']
COINS_LIMIT = settings['trade']['coins_limit']


def buy(client: Client,
        symbol: str,
        qty: float,
        min_notional: Decimal) -> Client.order_market_buy:
    try:
        if qty > min_notional:
            #  TODO: logs in postgresql
            client.order_market_buy(symbol=symbol, quantity=qty)
            # create.purchased_coin(symbol, qty, rate)
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


def buy_process(client: Client) -> None:
    coins: tuple = scan(client.get_ticker())
    for coin in coins:
        current_price: Decimal = Decimal(
            client.get_symbol_ticker(symbol=coin).get('price')
        )
        rising: bool = analysis(
            prices=get_prices(client, coin),
            current_price=current_price
        )
        if rising and get.coins_limit(COINS_LIMIT) and get.purchased_coin_doesnt_exist(coin):
            qty = get_qty(
                client=client,
                coin=coin,
                price=PRICE_TO_BUY
            )
            buy(
                client=client,
                symbol=coin,
                qty=qty,
                min_notional=get_min_notional(client=client)
            )
