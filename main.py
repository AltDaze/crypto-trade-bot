# -*- coding: utf-8 -*-

import asyncio
import configparser
import os
from configparser import ConfigParser

import yaml
from binance import Client

from modules.trade.binance.buy.main import buy_process
from modules.trade.binance.sell.main import sell_process

with open('{0}/../../../../settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

config: ConfigParser = configparser.ConfigParser()
config.read('config.ini'.format(os.path.dirname(__file__)))

API_KEY = config['binance']['api_key']
API_SECRET = config['binance']['api_secret']

_client: Client = Client(API_KEY, API_SECRET, {"verify": True, "timeout": 20})


class Settings:
    DEFAULT_PAIR: str = settings['trade']['default_pair']
    PRICE_TO_BUY: float = settings['trade']['price_to_buy']
    COINS_LIMIT: int = settings['trade']['coins_limit']


def main(client: Client):
    # TODO:
    #  1. Асинхронность
    #  3. Добавить возможность покупать на "фантики"
    #  4. Добавить бекенд и сверстать страницу с анализом
    #  5. Remove exception_handle in database /
    #    / Оставить чтобы отлавливать неизвестные ошибки, но в случае чего писать свои try/except
    #  6. ВАЖНО КОРОЧЕ POSTGRESQL / ASYNCIO / LOGGER / VENV
    #  7. postgresql or mysql?
    #  8. МБ все же стоит сделать на sqlite и просто хорошо продумать модели)
    #  9. Добаить type hitting
    #  10. Написать декоратор, который дает доступ к настройкам исходя из текущего файла автоматически \
    #  Либо создать класс со всеми нужными настройками
    # create.database()
    # create.table()
    while True:
        buy_process(client)
        sell_process(client)


if __name__ == "__main__":
    asyncio.run(main(_client))
