from decimal import Decimal
from modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def create_database(con):
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS TRADES
        (SYMBOL TEXT NOT NULL,
        AMOUNT DECIMAL NOT NULL,
        RATE DECIMAL NOT NULL,
        HIGHEST_PRICE DECIMAL NOT NULL);'''
    )


@exception_handler
@with_connection
def purchased_coin(con, symbol: str, amount: Decimal, rate: Decimal):
    cur = con.cursor()
    cur.execute(
        'INSERT INTO TRADES(SYMBOL, AMOUNT, RATE, HIGHEST_PRICE) VALUES (?, ?, ?, ?)',
        [symbol, amount, rate, rate]
    )
