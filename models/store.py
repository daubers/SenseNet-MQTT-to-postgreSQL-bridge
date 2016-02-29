from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Store(Base):
    """
        A generic data store
    """
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    topic = Column(UnicodeText)
    payload = Column(UnicodeText)
