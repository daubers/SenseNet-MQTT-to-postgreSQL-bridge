from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    engine = create_engine('postgresql://user:pass@localhost:5432/sensenet')
    return engine


def get_session():
    db_session = sessionmaker(bind=get_engine())
    return db_session()

