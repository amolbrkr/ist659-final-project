import random

# Rank cards for evaluation
def rank_hand(hand):
    values = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    value_count = {value: values.count(value) for value in values}

    # Pair or Three of a Kind
    for value, count in value_count.items():
        if count == 3:
            return 4, value  # Three of a Kind
        if count == 2:
            return 3, value  # Pair

    # Straight Flush or Straight
    if all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1)):
        if len(set(suits)) == 1:
            return 5, max(values)  # Straight Flush
        else:
            return 2, max(values)  # Straight

    # Flush
    if len(set(suits)) == 1:
        return 1, max(values)  # Flush

    # High Card
    return 0, max(values)

# Deal cards
def deal_hand():
    deck = [(value, suit) for value in range(2, 15) for suit in ['H', 'D', 'C', 'S']]
    random.shuffle(deck)
    return sorted(deck[:3])

# Main game loop
while input("Wanna play 3-Card Poker? 'y' or 'n': ") == 'y':
    player_hand = deal_hand()
    dealer_hand = deal_hand()

    print(f"Your hand: {player_hand}")
    print(f"Dealer's hand: {dealer_hand}")

    player_rank, player_high = rank_hand(player_hand)
    dealer_rank, dealer_high = rank_hand(dealer_hand)

    print(f"Your rank: {player_rank}, high card: {player_high}")
    print(f"Dealer's rank: {dealer_rank}, high card: {dealer_high}")

    if player_rank > dealer_rank:
        print("You win. Congrats, or whatever.")
    elif player_rank < dealer_rank:
        print("Dealer wins. You lose. Surprise, surprise.")
    else:
        if player_high > dealer_high:
            print("You win on a high card. Lucky you.")
        elif player_high < dealer_high:
            print("Dealer wins on a high card. What did you expect?")
        else:
            print("It's a tie. How unexciting.")