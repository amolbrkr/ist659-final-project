import os
import hashlib
from models.models import Player, Lobby, CardPlayed, PlayerMove, Bid, DealerCard
from models.request_models import PlayerCreate, PlayerLogin
from models.functions import create_deck, rank_hand, update_player_balance
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
            status="WAITING",  # Set the initial status
            hostPlayerId=hostplayerID,  # Set the host player's ID
            turn = 0
        )
        db.add(new_lobby)
        db.commit()
        print(vars(new_lobby))
        return new_lobby
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )

##### NO LONGER NEEDED
# @app.post("/join-lobby")
# async def join_lobby(playerId: int, lobbyId: int):
#     # try:
#     player = db.query(Player).filter(Player.id == playerId).first()

#     if player is None:
#         raise HTTPException(status_code=404, detail="Player not found.")

#     lobby = db.query(Lobby).filter(Lobby.id == lobbyId).first()

#     if lobby is None:
#         raise HTTPException(status_code=404, detail=f"No lobby with id: {lobbyId}")

#     # Add a check to see if player is already in lobby
#     if lobby.currentPlayers < lobby.maxPlayers:
#         lobby.currentPlayers += 1
#         db.add(PlayerLobby(player_id=playerId, lobby_id=lobbyId))
#         db.commit()

#         return {"message": "Player joined the lobby."}
#     else:
#         return {"message": f"Lobby {lobbyId} is full."}

#     # except Exception as err:
#     #     raise HTTPException(
#     #         status_code=500, detail=f"Something went wrong, error: {str(err)}"
#     #     )


@app.post("/deal-cards")
async def deal_cards(lobby_id: int, ante_amount: int):
    current_lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
    player_id = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()

    # update balance in player table
    current_player = db.query(Player).filter(Player.id == player_id).first()
    if current_player.balance < ante_amount:
        return {"error": "Not enough funds"}
    else:
        update_player_balance(player_id, -ante_amount,db)

    # Update the turn and commit
    new_turn = current_lobby.turn + 1
    current_lobby.turn = new_turn

    # Create new instance of PlayerMove
    PlayerMove = PlayerMove(
        lobby_id = lobby_id,
        lobby_turn = new_turn,
        amount = ante_amount,
        winner = 'none',
        balance_result = -ante_amount
    )
    db.add(PlayerMove)

    # create deck and deal cards
    deck = create_deck()
    lobby_hand = deal_cards(deck)
    player_hand = deal_cards(deck)
    shuffle(lobby_hand)

    #  Update cardsplayed in database
    for card in player_hand:
        card_rank = card[0]
        card_suit = card[1]
        CardPlayed=CardPlayed(
            lobby_id = lobby_id,
            lobby_turn = new_turn,
            card_rank = card_rank,
            card_suite = card_suit,
            entity = 'Player'
        )
        db.add(CardPlayed)
    for card in lobby_hand:
        card_rank = card[0]
        card_suit = card[1]
        CardPlayed=CardPlayed(
            lobby_id = lobby_id,
            lobby_turn = new_turn,
            card_rank = card_rank,
            card_suite = card_suit,
            entity = 'Dealer'
        )
        db.add(CardPlayed)
    
    #commit all changes to the database
    db.commit()
    # return the info to the front end 
    return {
        "lobby": lobby_id,
        "turn": new_turn,
        "lobby_hand": lobby_hand,
        "player_hand": player_hand,
    }



@app.post("/play")
async def play(lobby_id: int, turn: int):
    player_id = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
    # queries to get the player and dealer hand
    player_hand_query = (
        db.query(CardPlayed.card_rank, CardPlayed.card_suite)
        .filter(
            CardPlayed.player_id == player_id,
            CardPlayed.lobby_id == lobby_id,
            CardPlayed.turn == turn,
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
            outcome = "tie"
   
    ## update the database
    PlayerMove = db.query(PlayerMove).filter(lobby_id = lobby_id, lobby_turn = turn)
    ante_amount = PlayerMove.amount
    if outcome == "player_win":
        update_player_balance(player_id, 2*ante_amount,db)
        PlayerMove.winner = 'Player'
    elif outcome == "tie":
        update_player_balance(player_id, ante_amount,db)
        PlayerMove.winner = 'tie'
    else:
        PlayerMove.winner = 'Dealer'
    
    # commit changes to database
    db.commit()

    # get new player balance
    updated_player_balance = db.query(Player.balance).filter(Player.id == player_id).first()
    
    # output to frontend
    return {"outcome": outcome,
            "balance": updated_player_balance}
    #### HERE NEED TO STORE THE RESULT IN THE DATABASE

@app.post("/fold")
async def fold(lobby_id: int, turn: int):
    # Get the player by ID
    player_id = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
    PlayerMove = db.query(PlayerMove).filter(lobby_id = lobby_id, lobby_turn = turn)
    ante_amount = PlayerMove.amount
    if player_id:
        # Update the player's balance by subtracting the ante amount
        update_player_balance(player_id, ante_amount,db)

        # Commit the changes to the database
        db.commit()
        
        # get updated balance
        updated_player_balance = db.query(Player.balance).filter(Player.id == player_id).first()
        
        # output to frontend
        return {"balance": updated_player_balance}
    else:
        return {"error": "Player not found"}
