# -*- coding: utf-8 -*-

import os
from decimal import Decimal

import yaml

with open("{0}/../../settings.yaml".format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

GROWTH_FROM = settings['trade']['growth_range']['from']
GROWTH_TO = settings['trade']['growth_range']['to']


def scan(tickers: list = None) -> tuple:
    # The function returns the current coins with the price to BUSD and the exchange rate
    symbols: list = []
    for ticker in tickers:
        growth: Decimal = Decimal(ticker['priceChangePercent'])
        symbol: str = ticker.get("symbol")
        if symbol.endswith('BUSD') and GROWTH_FROM < growth < GROWTH_TO:
            symbols.append(symbol)
    return tuple(symbols)
