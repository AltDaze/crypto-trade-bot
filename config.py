# -*- coding: utf-8 -*-

import configparser
import os
from configparser import ConfigParser
from typing import Final

import yaml

with open('{0}/settings.yaml'.format(os.path.dirname(__file__)), 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

config: ConfigParser = configparser.ConfigParser()
config.read('config.ini'.format(os.path.dirname(__file__)))


class ClientSettings:
    API_KEY: Final = os.getenv('BINANCE_API_KEY')
    API_SECRET: Final = os.getenv('BINANCE_API_SECRET')
    API_PARAMS: Final = {"verify": True, "timeout": 20}


class Settings:
    DEFAULT_PAIR: str = settings['trade']['default_pair']
    PRICE_TO_BUY: float = settings['trade']['price_to_buy']
    COINS_LIMIT: int = settings['trade']['coins_limit']


class Database:
    DATABASE: Final = settings['database']['database']
    USER: Final = settings['database']['user']
    PASSWORD: Final = settings['database']['password']
    HOST: Final = settings['database']['host']
    PORT: Final = settings['database']['port']
