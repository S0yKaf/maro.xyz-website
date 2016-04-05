from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, create_session

engine = None
metadata = MetaData()

db_session = scoped_session(
    lambda: create_session(autocommit=False, autoflush=False, bind=engine))


def init_engine(uri):
    global engine
    engine = create_engine(uri, convert_unicode=True)
    return engine


def init_db():
    global engine
    metadata.create_all(bind=engine)
