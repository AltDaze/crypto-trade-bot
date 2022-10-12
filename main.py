# -*- coding: utf-8 -*-

import asyncio
from modules.trade.buy import buy_process
from modules.trade.sell import sell_process
from modules.database.create import create_database


def main():
    # TODO:
    #  1. Асинхронность
    #  2. Разделить конфиг и настройки на разные файлы, чтобы было управление через JavaFX
    #  3. Добавить возможность покупать на "фантики"
    create_database()
    while True:
        buy_process()
        sell_process()


if __name__ == "__main__":
    asyncio.run(main())
