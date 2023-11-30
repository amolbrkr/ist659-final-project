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
DATABASE_URL = "mssql+pyodbc://ffrancoa:DatabaseDictators23@ist659ffrancoa.database.windows.net:1433/poker?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()


query=session.query(Player).first()


# Check if the query returned a Player instance
if query:
    # Iterate over the attributes of the Player instance
    for column in Player.__table__.columns:
        # Print each attribute name and its value
        print(f"{column.name}: {getattr(query, column.name)}")
else:
    print("No player found.")