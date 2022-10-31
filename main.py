# -*- coding: utf-8 -*-

import asyncio

from binance import Client

from config import ClientSettings
from modules.trade.binance.buy.main import buy_process
from modules.trade.binance.sell.main import sell_process

_client: Client = Client(
    api_key=ClientSettings.API_KEY,
    api_secret=ClientSettings.API_SECRET,
    requests_params=ClientSettings.API_PARAMS
)


def main(client: Client):
    # TODO:
    #  1. Асинхронность
    #  3. Demo Счет
    #  5. Remove exception_handle in database /
    #    / Оставить чтобы отлавливать неизвестные ошибки, но в случае чего писать свои try/except
    #  6. ВАЖНО КОРОЧЕ POSTGRESQL / ASYNCIO / LOGGER / VENV
    #  7. postgresql or mysql?
    #  8. МБ все же стоит сделать на sqlite и просто хорошо продумать модели)
    #  9. Добаить type hitting
    #  10. Написать декоратор, который дает доступ к настройкам исходя из текущего файла автоматически \
    #  Либо создать класс со всеми нужными настройками
    #  Процент для покупки и продажи должен быть гибким, а не фиксированым и складываться из неких факторов
    # create.database()
    # create.table()
    while True:
        buy_process(client)
        sell_process(client)


if __name__ == "__main__":
    asyncio.run(main(_client))
