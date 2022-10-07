# -*- coding: utf-8 -*-

import sqlite3
import decimal


def create_database():
    # TODO: use 1. PostgreSQL 2. SQLAlchemy
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS trades (
                symbol TEXT,
                amount DECIMAL,
                rate DECIMAL,
                highest_price DECIMAL
                )
            """
        )
        conn.commit()
