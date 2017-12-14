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

class Invite():
    query = db_session.query_property()

    def __init__(self, code, creator_id):
        self.code = code
        self.creator_id = creator_id

    def __repr__(self):
        return '<Invite %r>' % (self.code)


uploads = Table('uploads', metadata,
                Column('id', Integer, primary_key=True),
                Column('hash', Binary(20), unique=True),
                Column('short_url', String(7), unique=True),
                Column('mime_type', String(255)),
                Column('blocked', Boolean, default=False),
                )

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(255), unique=True),
              Column('password', Binary(64)),
              Column('salt', String(42)),
              Column('token', String(32)),
              Column('is_admin', Boolean, default=False),
              )

invites = Table('invites', metadata,
                Column('id', Integer, primary_key=True),
                Column('code', String(32), unique=True),
                Column('creator_id', Integer),
                Column('redeemed', Boolean, default=False),
                )

mapper(Upload, uploads)
mapper(User, users)
mapper(Invite, invites)
