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


player_hand_query = session.query(PlayerCard.card_rank, PlayerCard.card_suite).filter(
    PlayerCard.player_id == 1,
    PlayerCard.lobby_id == 1
).all()
player_hand = [(card_rank, card_suite) for card_rank, card_suite in player_hand_query]

dealer_hand_query = session.query(DealerCard.card_rank, DealerCard.card_suite).filter(
    DealerCard.lobby_id == 1
).all()
dealer_hand = [(card_rank, card_suite) for card_rank, card_suite in dealer_hand_query]
print(dealer_hand_query)
print(player_hand)
print(dealer_hand)

player_rank, player_high = rank_hand(player_hand)
dealer_rank, dealer_high = rank_hand(dealer_hand)

print(player_rank)
print(dealer_rank)

outcome = None
if player_rank > dealer_rank:
    outcome = "player_win"
elif player_rank < dealer_rank:
    outcome = "dealer_win"
else:
    if player_high > dealer_high:
        outcome = "player_win"
    elif player_high < dealer_high:
        outcome = "dealer_win"
    else:
        outcome = "dealer_win"
print(outcome)