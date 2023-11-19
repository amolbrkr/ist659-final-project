import random
from sqlalchemy.orm import Session
from typing import List, Tuple
from models.models import CardPlayed, Player


# Define a function to create and return a deck of cards
def create_deck():
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    deck = [[rank, suit] for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck


# Define a function to draw three cards
def deal_hand(deck):
    hand = deck[:3]
    del deck[:3]
    return hand


# define a function to get the rank values of cards
def rank_card(card_rank):
    rank_map = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    return rank_map.get(card_rank, 0)  # Using the first character as the key, return 0 if not found.


# Define a funtion to rank hand
def rank_hand(hand):
    values = [rank_card(card[0]) for card in hand]
    suits = [card[1] for card in hand]
    value_count = {value: values.count(value) for value in values}

    for value, count in value_count.items():
        if count == 3:
            return 4, value
        if count == 2:
            return 3, value

    if all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1)):
        if len(set(suits)) == 1:
            return 5, max(values)
        else:
            return 2, max(values)

    if len(set(suits)) == 1:
        return 1, max(values)

    return 0, max(values)


# function to get a player hand
def get_player_hand(
    db: Session, player_id: int, lobby_id: int
) -> List[Tuple[str, str]]:
    query = (
        db.query(CardPlayed.card_rank, CardPlayed.card_suite)
        .filter(CardPlayed.player_id == player_id, CardPlayed.lobby_id == lobby_id,entity='Player')
        .all()
    )

    if not query:
        return []  # Or some other default value, maybe raise an exception

    hand = [(card_rank, card_suite) for card_rank, card_suite in query]
    return hand

# function to update player balance
def update_player_balance(player_id, amount,db):
    player = db.query(Player).filter(Player.id == player_id).first()
    player.balance += amount


# hand = deal_hand(create_deck())

# # hand = [['K', 'Diamonds'], ['A', 'Diamonds'], ['K', 'Clubs']]
# print(hand)

# rank=(rank_hand(hand))
# print(rank)