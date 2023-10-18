from models import *
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

for row in session.query(Lobby).all():
    print(vars(row))
