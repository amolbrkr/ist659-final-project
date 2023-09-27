from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Card(base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    suit = Column(String, nullable=False)
    rank = Column(String, nullable=False)