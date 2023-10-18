import random
from typing import List, Tuple


def deal_hand() -> List[Tuple[int, str]]:
    card_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    deck = [(card_rank, card_suit) for card_rank in card_ranks for card_suit in ['hearts', 'diamonds', 'clubs', 'spades']]
    random.shuffle(deck)
    return sorted(deck[:3])

