# -*- coding: utf-8 -*-

import asyncio

from modules.trade.binance.buy.buy import buy_process
from modules.trade.binance.sell.sell import sell_process
from modules.analysis.scan import scan


def main():
    # TODO:
    #  1. Асинхронность
    #  3. Добавить возможность покупать на "фантики"
    #  4. Добавить бекенд и сверстать страницу с анализом
    #  5. Remove exception_handle in database /
    #    / Оставить чтобы отлавливать неизвестные ошибки, но в случае чего писать свои try/except
    #  6. ВАЖНО КОРОЧЕ POSTGRESQL / ASYNCIO / LOGGER / VENV
    #  7. postgresql or mysql?
    # create.database()
    # create.table()
    while True:
        buy_process()
        sell_process()


if __name__ == "__main__":
    asyncio.run(main())
