from decimal import Decimal
from modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def historically_highest_coin_value(con, symbol: str, price: Decimal):
    cur = con.cursor()
    current_highest_price = cur.execute(
        'SELECT HIGHEST_PRICE FROM TRADES WHERE SYMBOL = ?',
        [symbol]
    )
    chp = current_highest_price.fetchone()[0]
    if price > chp:
        cur.execute(
            'UPDATE TRADES SET HIGHEST PRICE = ? WHERE SYMBOL = ?',
            [price, symbol]
        )
