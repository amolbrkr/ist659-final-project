import os
import hashlib
from models.models import Player, Lobby, PlayerCard, PlayerLobby, Bid, DealerCard
from models.request_models import PlayerCreate, PlayerLogin
from models.functions import create_deck, rank_hand
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

        return {
            "loginSuccess": True,
            "player": player.id,
            "firstname": player.firstname,
            "lastname": player.lastname,
            "username": player.username,
            "balance": player.balance,
        }

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Player name already exists")
    finally:
        db.close()


@app.post("/login")
async def login(player: PlayerLogin):
    try:
        pwHash = hashlib.sha256(player.password.encode("utf-8")).hexdigest()
        p = (
            db.query(Player)
            .filter(
                Player.username == player.username,
                Player.passwordHash == pwHash,
            )
            .first()
        )

        if p is None:
            raise HTTPException(
                status_code=404,
                detail="Player not found, check username or password.",
            )

        return {
            "loginSuccess": True,
            "player": p.id,
            "firstname": p.firstname,
            "lastname": p.lastname,
            "username": p.username,
            "balance": p.balance,
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
            currentPlayers=1,  # Set the initial number of current players
            maxPlayers=5,  # Set the maximum number of players
            status="WAITING",  # Set the initial status
            hostPlayerId=hostplayerID,  # Set the host player's ID
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
    current_lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
    # Update the turn and commit
    new_turn = current_lobby.turn + 1
    current_lobby.turn = new_turn
    db.commit()
    Player = session.query(Lobby).filter(Player.id == lobby_id).first()
    deck = create_deck()
    lobby_hand = deal_cards(deck)
    player_hand = deal_cards(deck)
    shuffle(lobby_hand)
    return {
        "lobby": lobby_id,
        "turn": new_turn,
        "lobby_hand": lobby_hand,
        "player_hand": player_hand,
    }


def update_player_balance(player_id, amount):
    player = db.query(Player).filter(Player.id == player_id).first()
    player.balance += amount
    db.commit()


@app.post("/play")
async def play(lobby_id: int, player_id: int, action: str, turn: int, ante_amount: int):
    player = db.query(Player).filter(Player.id == player_id).first()

    # Call the function to make the ante bet with custom_amount (before play)
    update_player_balance(player_id, -1 * ante_amount)
    ante_bid = Bid(
        player_id=player.id,  # Set the player ID
        lobby_id=lobby_id,  # Set the lobby or game ID
        bid_type="Ante",  # Set the bid type
        amount=ante_amount,
    )
    db.add(ante_bid)
    db.commit()
    # queries to get the player and dealer hand
    player_hand_query = (
        db.query(PlayerCard.card_rank, PlayerCard.card_suite)
        .filter(
            PlayerCard.player_id == player_id,
            PlayerCard.lobby_id == lobby_id,
            PlayerCard.turn == turn,
        )
        .all()
    )
    player_hand = [
        (card_rank, card_suite) for card_rank, card_suite in player_hand_query
    ]

    dealer_hand_query = (
        db.query(DealerCard.card_rank, DealerCard.card_suite)
        .filter(DealerCard.lobby_id == lobby_id, DealerCard.turn == turn)
        .all()
    )
    dealer_hand = [
        (card_rank, card_suite) for card_rank, card_suite in dealer_hand_query
    ]

    # rank the hands
    player_rank, player_high = rank_hand(player_hand)
    dealer_rank, dealer_high = rank_hand(dealer_hand)

    # compare the ranks
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
            return {"outcome": outcome}


@app.post("/fold")
async def fold(player_id, ante_amount):
    # Get the player by ID
    player = db.query(Player).filter(Player.id == player_id).first()

    if player:
        # Update the player's balance by subtracting the ante amount
        player.balance -= ante_amount

        # Commit the changes to the database
        db.commit()

        return {"balance": player.balance}
    else:
        return {"error": "Player not found"}
