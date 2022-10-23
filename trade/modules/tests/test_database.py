# from trade.modules.database.other import with_connection
#
#
# @with_connection
# def create_database(cursor):
#     sql = 'create database postgres'
#     cursor.execute(sql)
#
#
# @with_connection
# def create_table(cursor):
#     cursor.execute(
#         '''create table "postgres";'''
#     )
#
#
# @with_connection
# def insert(cursor):
#     #  TODO: Создать таблицу с логами, где будет показываться
#     #   когда, что и сколько покупалось/продавалось
#     cursor.execute(
#         "insert into trades (symbol, amount, demo) values (%s, %s, %s);",
#         ['XMRBUSD', 0.25, True]
#     )
#
#
# @with_connection
# def select(cursor):
#     result = cursor.execute(
#         'SELECT * FROM TRADES'
#     ).fetchall()
#     return result
#
#
# @with_connection
# def select_tables(cursor):
#     tables = cursor.execute("""SELECT table_name FROM information_schema.tables
#            WHERE table_schema = 'public'""").fetchall()
#     return tables
#
#
# insert()
