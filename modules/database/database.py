# -*- coding: utf-8 -*-

import sqlite3
import decimal


def create_database():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS trades (
                symbol TEXT,
                amount DECIMAL,
                rate DECIMAL,
                highest_price DECIMAL
                )
            """
        )
        conn.commit()


def database_connect(func):
    def connect(*args):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            function = func(*args, cursor)
            conn.commit()
            return function

    return connect


@database_connect
def purchased_coin(symbol: str, amount: decimal, rate: decimal, cur):
    # adding the purchased coin to the database
    try:
        cur.execute(
            'INSERT INTO trades(symbol, amount, rate, highest_price) VALUES (?, ?, ?, ?)',
            [symbol, amount, rate, rate]
        )
    except Exception as e:
        print('[!]', e)


@database_connect
def update_historically_highest_coin_value(symbol: str, price: decimal, cur):
    # TODO: Заменить всю конструкцию одним sql запросом
    try:
        current_highest_price = cur.execute(
            'SELECT highest_price FROM trades WHERE symbol = ?', [symbol]
        ).fetchone()[0]
        if price > current_highest_price:
            cur.execute(
                'UPDATE trades SET highest_price = ? WHERE symbol = ?',
                [price, symbol]
            )
    except Exception as e:
        print('[!]', e)


@database_connect
def get_historically_highest_coin_price(symbol: str, cur) -> decimal:
    try:
        return cur.execute('SELECT highest_price FROM trades WHERE symbol = ?',
                           [symbol]).fetchone()[0]
    except Exception as e:
        print('[!]', e)


@database_connect
def get_the_number_of_purchased_coins(symbol: str, cur) -> decimal:
    try:
        return cur.execute('SELECT amount FROM trades WHERE symbol = ?',
                           [symbol]).fetchone()[0]
    except Exception as e:
        print('[!]', e)


@database_connect
def get_rate_of_symbol(symbol: str, cur) -> decimal:
    try:
        return cur.execute('SELECT rate FROM trades WHERE symbol = ?',
                           [symbol]).fetchone()[0]
    except Exception as e:
        print('[!]', e)


@database_connect
def coins_limit(limit: int, cur) -> bool:
    # Checking if the limit on purchased coins has been exceeded
    try:
        rows = cur.execute('SELECT * FROM trades').fetchall()
        coins = [row[0] for row in rows]
        return True if limit > len(coins) and limit != 0 else False
    except Exception as e:
        print('[!]', e)


@database_connect
def coins_amount(cur) -> int:
    # Number of coins purchased
    try:
        rows = cur.execute('SELECT * FROM trades').fetchall()
        coins = []
        for row in rows:
            coins.append(row[0])
        return len(coins)
    except Exception as e:
        print('[!]', e)


@database_connect
def remove_purchased_coin(symbol: str, cur):
    try:
        cur.execute(
            'DELETE FROM trades WHERE symbol = ?', [symbol]
        )
    except Exception as e:
        print('[!]', e)


@database_connect
def purchased_coin_doesnt_exist(symbol: str, cur) -> bool:
    try:
        s = cur.execute(
            'SELECT symbol FROM trades WHERE symbol = ?',
            [symbol]
        ).fetchone()
        if s is None:
            return True
        else:
            return False
    except Exception as e:
        print(e)


@database_connect
def get_the_names_of_purchased_coins(cur) -> list:
    try:
        info = cur.execute('SELECT symbol FROM trades').fetchall()
        result = [i[0] for i in info]
        return result
    except Exception as e:
        print('[!]', e)
