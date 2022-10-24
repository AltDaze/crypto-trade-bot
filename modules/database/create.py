from decimal import Decimal

import psycopg2

from modules.database.other import with_connection, exception_handler


@with_connection
def database(cursor):
    try:
        sql = 'CREATE database trades'
        cursor.execute(sql)
    except psycopg2.errors.DuplicateDatabase:
        pass


@with_connection
def table(cursor):
    pass
    # cursor.execute(
    #     '''
    #     CREATE TABLE IF NOT EXISTS TRADES (
    #     deal_id SERIAL PRIMARY KEY,
    #     trade_datetime DATE,
    #     demo BOOLEAN DEFAULT false
    #     coin TEXT NOT NULL,
    #     amount DECIMAL NOT NULL,
    #     rate DECIMAL NOT NULL,
    #
    #     )
    #     (SYMBOL TEXT NOT NULL,
    #     AMOUNT DECIMAL NOT NULL,
    #     RATE DECIMAL NOT NULL,
    #     HIGHEST_PRICE DECIMAL NOT NULL);
    #     '''  # Переписать highest_price, сделать алгоритм, который будет искать наивысшую стоимость
    # )
    # cur.execute(
    #     # TODO:
    #     #  Таблица должна быть построчная
    #     #  Со временем покупки и продажи в одной строке
    #     #  Так же считать прибыль
    #     #  Пометка ДЕМО для прокрутки на фантики
    #     '''CREATE TABLE IF NOT EXISTS LOGS
    #     (DATETIME DATETIME NOT NULL,
    #     AMOUNT DECIMAL NOT NULL,
    #     RATE DECIMAL NOT NULL,
    #     HIGHEST_PRICE DECIMAL NOT NULL);'''
    # )


@exception_handler
@with_connection
def purchased_coin(cursor, symbol: str, amount: Decimal, rate: Decimal):
    #  TODO: Создать таблицу с логами, где будет показываться
    #   когда, что и сколько покупалось/продавалось
    cursor.execute(
        'INSERT INTO TRADES(SYMBOL, AMOUNT, RATE, HIGHEST_PRICE) VALUES (?, ?, ?, ?)',
        [symbol, amount, rate, rate]
    )
