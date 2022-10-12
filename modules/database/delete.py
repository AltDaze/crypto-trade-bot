from decimal import Decimal
from modules.database.other import with_connection, exception_handler


@exception_handler
@with_connection
def purchased_coin(con, symbol: str, amount: Decimal, rate: Decimal):
    cur = con.cursor()
    cur.execute(
        'DELETE FROM trades WHERE symbol = ?',
        [symbol]
    )