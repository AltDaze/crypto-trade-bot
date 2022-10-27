# -*- coding: utf-8 -*-

from binance import Client
from decimal import Decimal
from binance.helpers import round_step_size


def get_prices(client: Client, coin: str) -> tuple:
    candles: dict = client.get_klines(
        symbol=coin,
        interval=client.KLINE_INTERVAL_3MINUTE,
        limit=500
    )
    prices: tuple = tuple([candle[2] for candle in candles])
    return prices


def get_symbol_info(client: Client, coin: str) -> dict:
    symbol_info: dict = client.get_symbol_info(coin).get("filters")
    return symbol_info


def get_min_notional(client: Client, symbol_info: dict) -> Decimal:
    min_notional: Decimal = Decimal(
        symbol_info[3].get('minNotional')
    )
    return min_notional


def get_qty(client: Client, coin: str, price: Decimal) -> float:
    symbol_info: dict = get_symbol_info(client=client, coin=coin)
    min_notional: Decimal = get_min_notional(client=client, symbol_info=symbol_info)
    step_size: Decimal = Decimal(
        symbol_info[2].get('stepSize')
    )
    rate: Decimal = Decimal(
        client.get_symbol_ticker(symbol=coin).get('price')

    )
    amount: Decimal = 1 / rate * price
    qty: float = round_step_size(quantity=amount, step_size=step_size)
    return qty
