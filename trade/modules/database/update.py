from decimal import Decimal

from trade.modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def historically_highest_coin_value(cursor, symbol: str, price: Decimal):
    current_highest_price = cursor.execute(
        'SELECT HIGHEST_PRICE FROM TRADES WHERE SYMBOL = ?',
        [symbol]
    )
    chp = current_highest_price.fetchone()[0]
    if price > chp:
        cursor.execute(
            'UPDATE TRADES SET HIGHEST PRICE = ? WHERE SYMBOL = ?',
            [price, symbol]
        )
