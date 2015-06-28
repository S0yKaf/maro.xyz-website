from sqlalchemy import Table, Column, Integer, String, Binary
from sqlalchemy.orm import mapper
from database import metadata, db_session

class Upload(object):
    query = db_session.query_property()

    def __init__(self, hash, short_url, mime_type):
        self.hash = hash
        self.short_url = short_url
        self.mime_type = mime_type

    def __repr__(self):
        return '<Upload %r>' % (self.hash)


uploads = Table('uploads', metadata,
    Column('id', Integer, primary_key=True),
    Column('hash', Binary(20), unique=True),
    Column('short_url', String(7), unique=True),
    Column('mime_type', String(255))
)

mapper(Upload, uploads)
