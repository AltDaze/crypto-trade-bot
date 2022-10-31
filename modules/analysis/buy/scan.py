# -*- coding: utf-8 -*-

from decimal import Decimal

from config import Settings

GROWTH_RANGE_FROM = Settings.GROWTH_RANGE_FROM
GROWTH_RANGE_TO = Settings.GROWTH_RANGE_TO


def scan(tickers: list) -> tuple:
    # The function returns the current coins with the price to BUSD and the exchange rate
    symbols: list = []
    for ticker in tickers:
        growth: Decimal = Decimal(ticker['priceChangePercent'])
        symbol: str = ticker.get("symbol")
        if symbol.endswith('BUSD') and GROWTH_RANGE_FROM < growth < GROWTH_RANGE_TO:
            symbols.append(symbol)
    return tuple(symbols)
