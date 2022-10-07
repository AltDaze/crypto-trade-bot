# -*- coding: utf-8 -*-

import configparser
import modules.database as db
from modules.database import create_database
import traceback

from modules.trade.buy import buy
from modules.trade.sell import sell

from modules.analysis.scan import scan
# from modules.analysis import scan

config = configparser.ConfigParser()
config.read('config.ini')

COINS_LIMIT = config['settings'].getint('coins_limit')
PRICE_TO_BUY = config['settings'].getint('price_to_buy')


# def buy_process():
#     # The process of buying a coin
#     try:
#         for coin in scan():
#             if coin_analysis(coin) and db.coins_limit(COINS_LIMIT):
#                 buy_coin(symbol=coin, price=PRICE_TO_BUY)
#     except Exception:
#         print(traceback.format_exc())
#
#
# def sell_process():
#     # The process of selling a coin
#     try:
#         coins = db.get_the_names_of_purchased_coins()
#         for coin in coins:
#             if coin_relevance(coin):
#                 sell_coin(coin)
#     except Exception:
#         print(traceback.format_exc())


def main():
    # TODO:
    #  1. Асинхронность
    #  2. Разделить конфиг и настройки на разные файлы, чтобы было управление через JavaFX
    #  3. Добавить возможность покупать на "фантики"
    # db.create_database()
    print(scan())
    while True:
        pass
        # buy_process()
        # sell_process()


if __name__ == "__main__":
    main()
