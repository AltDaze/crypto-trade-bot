# -*- coding: utf-8 -*-

import asyncio

from modules.trade.buy import buy_process
from modules.trade.sell import sell_process


def main():
    # TODO:
    #  1. Асинхронность
    #  3. Добавить возможность покупать на "фантики"
    #  4. Добавить бекенд и сверстать страницу с анализом
    #  5. Remove exception_handle in database
    #  6. ВАЖНО КОРОЧЕ POSTGRESQL / ASYNCIO / LOGGER / VENV
    #  7. postgresql or mysql?

    # create.database()
    # create.table()
    while True:
        buy_process()
        sell_process()


if __name__ == "__main__":
    asyncio.run(main())
