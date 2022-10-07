from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/database'

engine = create_engine(DATABASE_URI)
Base = declarative_base()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
