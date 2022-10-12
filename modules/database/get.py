from decimal import Decimal
from modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def historically_highest_coin_price(con, symbol: str, price: Decimal) -> Decimal:
    cur = con.cursor()
    highest_price = cur.execute(
        'SELECT HIGHEST_PRICE FROM TRADES WHERE SYMBOL = ?',
        [symbol]
    )
    return highest_price.fetchone()[0]


@exception_handler
@with_connection
def the_number_of_purchased_coins(con, symbol: str) -> Decimal:
    cur = con.cursor()
    number = cur.execute(
        'SELECT amount FROM trades WHERE symbol = ?',
        [symbol]
    )
    n = number.fetchone()[0]
    return n


@exception_handler
@with_connection
def rate_of_symbol(con, symbol: str) -> Decimal:
    cur = con.cursor()
    rate = cur.execute(
        'SELECT rate FROM trades WHERE symbol = ?',
        [symbol])
    r = rate.fetchone()[0]
    return r


@exception_handler
@with_connection
def coins_limit(con, limit: int) -> bool:
    cur = con.cursor()
    rows = cur.execute('SELECT * FROM trades').fetchall()
    coins = [row[0] for row in rows]
    return True if limit > len(coins) and limit != 0 else False


@exception_handler
@with_connection
def coins_amount(con) -> int:
    cur = con.cursor()
    rows = cur.execute('SELECT * FROM trades').fetchall()
    coins = [row[0] for row in rows]
    return len(coins)


@exception_handler
@with_connection
def purchased_coin_doesnt_exist(con, symbol: str) -> bool:
    cur = con.cursor()
    s = cur.execute(
        'SELECT symbol FROM trades WHERE symbol = ?',
        [symbol]
    ).fetchone()
    return True if s is None else False


@exception_handler
@with_connection
def the_names_of_purchased_coins(con) -> list:
    cur = con.cursor()
    info = cur.execute('SELECT symbol FROM trades').fetchall()
    return [i[0] for i in info]