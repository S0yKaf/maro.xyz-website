from sqlalchemy import Table, Column, Integer, String, Binary, Boolean
from sqlalchemy.orm import mapper

from database import metadata, db_session


class Upload():
    query = db_session.query_property()

    def __init__(self, hash, short_url, mime_type):
        self.hash = hash
        self.short_url = short_url
        self.mime_type = mime_type

    def __repr__(self):
        return '<Upload %r>' % (self.hash)


class User():
    query = db_session.query_property()

    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % (self.username)


uploads = Table('uploads', metadata,
    Column('id', Integer, primary_key=True),
    Column('hash', Binary(20), unique=True),
    Column('short_url', String(7), unique=True),
    Column('mime_type', String(255)),
    Column('blocked', Boolean, default=False),
)

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255)),
    Column('password', Binary(64)),
    Column('salt', String(42)),
    Column('token', String(32)),
)

mapper(Upload, uploads)
mapper(User, users)
