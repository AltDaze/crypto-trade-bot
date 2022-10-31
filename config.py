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
    DEMO: bool = settings['trade']['demo']
    COINS_LIMIT: int = settings['trade']['coins_limit']
    PRICE_TO_BUY: float = settings['trade']['price_to_buy']
    DEFAULT_PAIR: str = settings['trade']['default_pair']
    SELL_FALL_PERCENTAGE: float = settings['trade']['sell']['fall_percentage']
    BUY_FALL_PERCENTAGE: float = settings['trade']['buy']['fall_percentage']
    GROWTH_RANGE_FROM: int = settings['trade']['growth_range']['from']
    GROWTH_RANGE_TO: int = settings['trade']['growth_range']['to']


class Database:
    DATABASE: Final = settings['database']['database']
    USER: Final = settings['database']['user']
    PASSWORD: Final = settings['database']['password']
    HOST: Final = settings['database']['host']
    PORT: Final = settings['database']['port']
