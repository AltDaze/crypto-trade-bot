from decimal import Decimal

from trade.modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def purchased_coin(cursor, symbol: str, amount: Decimal, rate: Decimal):
    cursor.execute(
        'DELETE FROM trades WHERE symbol = ?',
        [symbol]
    )
