import psycopg2
import traceback
from decimal import Decimal


def with_connection(f):
    def with_connection_(*args, **kwargs):
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        try:
            rv = f(con, *args, **kwargs)
        except Exception:
            con.rollback()
            raise
        else:
            con.commit()  # or maybe not
        finally:
            con.close()

        return rv

    return with_connection_


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
    return wrapper
