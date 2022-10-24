import traceback
from decimal import Decimal
from typing import Union

from modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def historically_highest_coin_price(cursor, symbol: str) -> Decimal:
    highest_price = cursor.execute(
        'SELECT HIGHEST_PRICE FROM TRADES WHERE SYMBOL = ?',
        [symbol]
    )
    return highest_price.fetchone()[0]


@exception_handler
@with_connection
def the_number_of_purchased_coins(cursor, symbol: str) -> Decimal:
    number = cursor.execute(
        'SELECT amount FROM trades WHERE symbol = ?',
        [symbol]
    )
    n = number.fetchone()[0]
    return n


@exception_handler
@with_connection
def rate_of_symbol(cursor, symbol: str) -> Decimal:
    rate = cursor.execute(
        'SELECT rate FROM trades WHERE symbol = ?',
        [symbol])
    r = rate.fetchone()[0]
    return r


@exception_handler
@with_connection
def coins_limit(cursor, limit: int) -> bool:
    rows = cursor.execute('SELECT * FROM trades').fetchall()
    coins = [row[0] for row in rows]
    return True if limit > len(coins) and limit != 0 else False


@exception_handler
@with_connection
def coins_amount(cursor) -> int:
    rows = cursor.execute('SELECT * FROM trades').fetchall()
    coins = [row[0] for row in rows]
    return len(coins)


@exception_handler
@with_connection
def purchased_coin_doesnt_exist(cursor, symbol: str) -> bool:
    symbols = cursor.execute(
        'SELECT symbol FROM trades WHERE symbol = ?',
        [symbol]
    ).fetchone()
    return True if symbols is None else False


@with_connection
def the_names_of_purchased_coins(cursor) -> Union[list, None]:
    try:
        info = cursor.execute('SELECT symbol FROM trades').fetchall()
        return [i[0] for i in info]
    except AttributeError:
        print(traceback.format_exc())
        return None
    finally:
        return None


@with_connection
def deal_time(deal_id: int = None) -> int:
    # TODO: НЕ ЗАБЫВАТЬ РЕАЛИЗОВАТЬ
    if deal_id is not None:
        pass
    pass
