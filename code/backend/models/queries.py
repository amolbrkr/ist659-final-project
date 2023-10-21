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

# Create a new Lobby instance
new_lobby = Lobby(currentPlayers=1, maxPlayers=5, status="WAITING", hostPlayerId=1)

# Add the new lobby to the session
session.add(new_lobby)

# Commit the transaction to save it to the database
session.commit()


#  Query the Lobby table for the specific record we added (based on some unique criteria, say hostPlayerId)
found_lobby = session.query(Lobby).filter_by(hostPlayerId=1).first()

# Print the details to confirm
if found_lobby:
    print(f"Lobby ID: {found_lobby.id}")
    print(f"Current Players: {found_lobby.currentPlayers}")
    print(f"Max Players: {found_lobby.maxPlayers}")
    print(f"Status: {found_lobby.status}")
    print(f"Host Player ID: {found_lobby.hostPlayerId}")
else:
    print("Hmm, looks like that lobby doesn't exist. Or you're in a parallel universe. Either way, weird.")