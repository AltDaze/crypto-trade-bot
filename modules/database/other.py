# -*- coding: utf-8 -*-

import configparser
import os
import traceback

import psycopg2
import yaml

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')

with open(os.path.dirname(__file__) + '/../../settings.yaml', 'r', encoding="utf8") as file:
    settings = yaml.safe_load(file)

DATABASE = settings['database']['database']
USER = settings['database']['user']
PASSWORD = settings['database']['password']
HOST = settings['database']['host']
PORT = settings['database']['port']


def with_connection(f):
    def with_connection_(*args, **kwargs):
        con = psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        con.autocommit = True
        cursor = con.cursor()
        try:
            rv = f(cursor, *args, **kwargs)
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
        finally:
            print(traceback.format_exc())

    return wrapper
