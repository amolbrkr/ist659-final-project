from models import *
from functions import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
# import pandas as pd
import os

# set directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(script_directory))))

# Define SQLAlchemy database connection
DATABASE_URL = "sqlite:///database/poker"  # Replace with your database URL
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()


# query = session.query(Player).filter(Player.id == 1).first()
query = session.query(func.count('*')).select_from(Lobby).filter(Lobby.hostPlayerId == 1).scalar()


print(query)
# for attr, value in player_stats.__dict__.items():
#     if not attr.startswith('_'):  # This will filter out SQLAlchemy's internal attributes
#             print(f"{attr}: {value}")
#     else:
#         print("No player found with ID 1")