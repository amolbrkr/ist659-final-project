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


session.add(PlayerCard(player_id=1, lobby_id=1, card_rank="A", card_suite="Hearts"))
session.add(PlayerCard(player_id=1, lobby_id=1, card_rank="K", card_suite="Clubs"))


# Commit these to the database
session.commit()

# Now, let's deal some cards to the dealer in a lobby
session.add(DealerCard(lobby_id=1, card_rank="2", card_suite="Hearts"))
session.add(DealerCard(lobby_id=1, card_rank="Q", card_suite="Diamonds"))
session.add(DealerCard(lobby_id=1, card_rank="9", card_suite="Clubs"))

# Commit these to the database
session.commit()