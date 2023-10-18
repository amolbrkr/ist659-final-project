import random

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def calculate_score(hand):
    if sum(hand) == 21 and len(hand) == 2:
        return 0
    if 11 in hand and sum(hand) > 21:
        hand.remove(11)
        hand.append(1)
    return sum(hand)

while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == 'y':
    user_hand = []
    computer_hand = []

    for _ in range(2):
        user_hand.append(deal_card())
        computer_hand.append(deal_card())

    game_over = False

    while not game_over:
        user_score = calculate_score(user_hand)
        computer_score = calculate_score(computer_hand)

        print(f"Your cards: {user_hand}, current score: {user_score}")
        print(f"Computer's first card: {computer_hand[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            should_continue = input("Type 'y' to get another card, 'n' to pass: ")
            if should_continue == 'y':
                user_hand.append(deal_card())
            else:
                game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_hand.append(deal_card())
        computer_score = calculate_score(computer_hand)

    print(f"Your final hand: {user_hand}, final score: {user_score}")
    print(f"Computer's final hand: {computer_hand}, final score: {computer_score}")

    if user_score > 21:
        print("You went over. You lose 😤")
    elif computer_score > 21:
        print("Computer went over. You win 😃")
    elif user_score == computer_score:
        print("It's a draw 🙃")
    elif user_score == 0:
        print("Blackjack! You win 😎")
    elif computer_score == 0:
        print("Computer got Blackjack. You lose 😭")
    elif user_score > computer_score:
        print("You win 😃")
    else:
        print("You lose 😤")