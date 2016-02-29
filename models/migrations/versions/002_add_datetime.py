from sqlalchemy import Column, DateTime, MetaData, Table
import datetime


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    store = Table('store', meta, autoload=True)
    datecol = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    datecol.create(store)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    store = Table('store', meta, autoload=True)
    store.c.timestamp.drop()
