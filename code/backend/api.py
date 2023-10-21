import os
import hashlib
from models.models import Player, Lobby, PlayerCard, PlayerLobby, Card, Bid, DealerCard
from models.request_models import PlayerCreate
from models.functions import create_deck, deal_hand, rank_hand, rank_card
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from random import shuffle

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(script_directory)))


DATABASE_URL = "sqlite:///database/poker"
engine = create_engine(DATABASE_URL)
db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# Initialize FastAPI
app = FastAPI()


@app.post("/create-player")
async def create_player(player: PlayerCreate):
    try:
        new_user = Player(
            firstname=player.firstname,
            lastname=player.lastname,
            username=player.username,
            passwordHash=hashlib.sha256(player.password.encode("utf-8")).hexdigest(),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Player name already exists")
    finally:
        db.close()


@app.post("/login")
async def login(username: str, password: str):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        player = (
            db.query(Player)
            .filter(Player.username == username, Player.passwordHash == password)
            .first()
        )

        if player is None:
            raise HTTPException(
                status_code=404,
                detail="Player not found, resubmit username or password.",
            )

        return {
            "loginSuccess": True,
            "player": player.id,
            "firstname": player.firstname,
            "lastname": player.lastname,
            "username": player.username,
            "balance": player.balance,
        }

    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )


@app.post("/create-lobby")
async def create_lobby(hostplayerID: int):
    player_list = [x[0] for x in db.query(Player.id).all()]
    if hostplayerID not in player_list:
        raise HTTPException(status_code=404, detail="Player does not exist.")

    try:
        # Assuming hostplayerID is the ID of the host player
        new_lobby = Lobby(
            currentPlayers=1,   # Set the initial number of current players
            maxPlayers=5,       # Set the maximum number of players
            status="WAITING",   # Set the initial status
            hostPlayerId=hostplayerID  # Set the host player's ID
        )
        db.add(new_lobby)
        db.commit()
        print(vars(new_lobby))
        return new_lobby
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )

 

@app.post("/join-lobby")
async def join_lobby(playerId: int, lobbyId: int):
    # try:
    player = db.query(Player).filter(Player.id == playerId).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found.")

    lobby = db.query(Lobby).filter(Lobby.id == lobbyId).first()

    if lobby is None:
        raise HTTPException(status_code=404, detail=f"No lobby with id: {lobbyId}")

    # Add a check to see if player is already in lobby
    if lobby.currentPlayers < lobby.maxPlayers:
        lobby.currentPlayers += 1
        db.add(PlayerLobby(player_id=playerId, lobby_id=lobbyId))
        db.commit()

        return {"message": "Player joined the lobby."}
    else:
        return {"message": f"Lobby {lobbyId} is full."}

    # except Exception as err:
    #     raise HTTPException(
    #         status_code=500, detail=f"Something went wrong, error: {str(err)}"
    #     )


# Define a function to deal three cards
@app.post("/deal-cards")
async def deal_cards(lobby_id: int):
    session = db
    Player = session.query(Lobby).filter(Player.id == lobby_id).first()
    deck = create_deck()
    lobby_hand = deal_cards(deck)
    player_hand = deal_cards(deck)
    shuffle(lobby_hand)
    return {"lobby": lobby_id, "lobby_hand": lobby_hand, "player_hand": player_hand}

def make_ante_bet(db, player, lobby_id, ante_bet_amt):
    
    # Create a new bid record in the 'bids' table
    ante_bid = Bid(
        player_id=player.id,  # Set the player ID
        lobby_id=lobby_id,    # Set the lobby or game ID
        bid_type='Ante',      # Set the bid type
        amount=ante_bet_amt
    )

    # Deduct the Ante bet amount from the player's balance
    player.balance -= ante_bet_amt

    db.add(ante_bid)
    db.commit()

    return ante_bid

def update_player_balance(player_id, amount):
    player = db.query(Player).filter(Player.id == player_id).first()
    player.balance += amount
    db.commit()

@app.post("/play")
async def play(lobby_id: int, player_id: int, ante_amount: int):
    player = db.query(Player).filter(Player.id == player_id).first()

    # Call the function to make the ante bet with custom_amount (before play)
    update_player_balance(player_id, -1 * ante_amount)
    ante_bid = Bid(
        player_id=player.id,  # Set the player ID
        lobby_id=lobby_id,    # Set the lobby or game ID
        bid_type='Ante',      # Set the bid type
        amount=ante_amount
    )
    db.add(ante_bid)
    db.commit()

    player_hand_query = db.query(PlayerCard.card_rank, PlayerCard.card_suite).filter(
        PlayerCard.player_id == player_id,
        PlayerCard.lobby_id == lobby_id
    ).all()
    player_hand = [(card_rank, card_suite) for card_rank, card_suite in player_hand_query]

    dealer_hand_query = db.query(DealerCard.card_rank, DealerCard.card_suite).filter(
        PlayerCard.lobby_id == lobby_id
    ).all()
    dealer_hand = [(card_rank, card_suite) for card_rank, card_suite in dealer_hand_query]

    player_rank, player_high = rank_hand(player_hand)
    dealer_rank, dealer_high = rank_hand(dealer_hand)

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
            return{"outcome": "dealer_win"}


# Simulate a player making an Ante bet
def make_ante_bet(player):
    ante_bet = 10.0  # Set the Ante bet amount (you can modify this)
    player.balance -= ante_bet
    return ante_bet

    # Call the function to make the play bet with custom_amount
    update_player_balance(player_id, ante_amount if outcome == "player_win" else -1 * ante_amount)
    return {"outcome": outcome, "ante_bid": ante_bid}
