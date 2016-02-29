from sqlalchemy import Column, Integer, UnicodeText, Table, MetaData

meta = MetaData()

store = Table(
    'store', meta,
    Column('id', Integer, primary_key=True),
    Column('topic', UnicodeText),
    Column('payload', UnicodeText)
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    store.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    store.drop()
