# -*- coding: utf-8 -*-

import psycopg2
import traceback
from decimal import Decimal
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DATABASE = config['database']['database']
USER = config['database']['user']
PASSWORD = config['database']['password']
HOST = config['database']['host']
PORT = config['database']['port']


def with_connection(f):
    def with_connection_(*args, **kwargs):
        con = psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
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
