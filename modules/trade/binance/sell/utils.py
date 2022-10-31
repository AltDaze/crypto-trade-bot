# -*- coding: utf-8 -*-

import traceback
from decimal import Decimal

from binance import Client

from modules.analysis.relevance import relevance
from modules.database.methods import get


def get_relevance(client: Client, coin: str) -> bool:
    try:
        deal_id: int = 0
        deal_time: int = get.deal_time(deal_id)
        exchange_rate: Decimal = Decimal(
            client.get_symbol_ticker(symbol=coin).get('price')
        )
        candles: dict = client.get_klines(
            symbol=coin,
            interval=client.KLINE_INTERVAL_3MINUTE,
            limit=1000,
            startTime=deal_time * 1000
        )
        highest_price: Decimal = Decimal(max([candle[2] for candle in candles]))
        return relevance(exchange_rate=exchange_rate, highest_price=highest_price)
    finally:
        print(traceback.format_exc())
        return False
