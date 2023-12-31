import os
import hashlib
from models.models import Player, Lobby, CardPlayed, PlayerMove
from models.request_models import PlayerLogin, PlayerCreate
from models.functions import create_deck, rank_hand, update_player_balance, deal_hand
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


DATABASE_URL = "mssql+pyodbc://ffrancoa:DatabaseLogin23@ffrancoa.database.windows.net:1433/poker?driver=ODBC+Driver+18+for+SQL+Server"
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


@app.get("/")
def default_route():
    return {"Status": "OK"}


@app.post("/create-player")
async def create_player(player: PlayerCreate):
    try:
        new_user = Player(
            firstname=player.firstname,
            lastname=player.lastname,
            username=player.username,
            passwordHash=hashlib.sha256(player.password.encode("utf-8")).hexdigest(),
            balance=1000,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "createSuccess": True,
            "player": new_user.id,
            "firstname": new_user.firstname,
            "lastname": new_user.lastname,
            "username": new_user.username,
            "balance": 1000,
        }

    except IntegrityError:
        raise HTTPException(status_code=400, detail="The username already exists")


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
                detail="Player not found, check your username or password.",
            )

        new_lobby = Lobby(
            status="WAITING",  # Set the initial status
            hostPlayerId=p.id,  # Set the host player's ID
            turn=0,
        )
        db.add(new_lobby)
        db.commit()

        new_lobby = db.query(Lobby).order_by(Lobby.id.desc()).first()
        return {
            "lobbyId": new_lobby.id,
            "lobbyTurn": 0,
            "loginSuccess": True,
            "player": p.id,
            "firstname": p.firstname,
            "lastname": p.lastname,
            "username": p.username,
            "balance": p.balance,
        }

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )


@app.post("/deal-cards")
async def deal_cards(lobby_id: int, ante_amount: int):
    try:
        current_lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
        if not current_lobby:
            raise HTTPException(status_code=404, detail="Lobby not found")

        player = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Host player not found")
        (player_id,) = player  # extract the player id

        # update balance in player table
        current_player = db.query(Player).filter(Player.id == player_id).first()
        if current_player.balance < ante_amount:
            return {"error": "Not enough funds"}
        else:
            update_player_balance(player_id, -ante_amount, db)

        # Update the turn and commit
        new_turn = current_lobby.turn + 1
        current_lobby.turn = new_turn

        # Create a new instance of PlayerMove
        new_PlayerMove = PlayerMove(
            lobby_id=lobby_id,
            lobby_turn=new_turn,
            amount=ante_amount,
            move_type="none",
            winner="none",
        )
        db.add(new_PlayerMove)

        # create deck and deal cards
        deck = create_deck()
        lobby_hand = deal_hand(deck)
        player_hand = deal_hand(deck)

        # Update cards played in the database
        for card in player_hand:
            card_rank = card[0]
            card_suit = card[1]
            player_CardPlayed = CardPlayed(
                lobby_id=lobby_id,
                lobby_turn=new_turn,
                card_rank=card_rank,
                card_suite=card_suit,
                entity="Player",
            )
            db.add(player_CardPlayed)
        for card in lobby_hand:
            card_rank = card[0]
            card_suit = card[1]
            dealer_CardPlayed = CardPlayed(
                lobby_id=lobby_id,
                lobby_turn=new_turn,
                card_rank=card_rank,
                card_suite=card_suit,
                entity="Dealer",
            )
            db.add(dealer_CardPlayed)

        # commit all changes to the database
        db.commit()

        # return the info to the front end
        return {
            "lobby": lobby_id,
            "turn": new_turn,
            "lobbyHand": lobby_hand,
            "playerHand": player_hand,
        }

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )


@app.post("/play")
async def play(lobby_id: int, turn: int):
    current_player = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
    if not current_player:
        raise HTTPException(status_code=404, detail="Host player not found")
    (player_id,) = current_player  # extract the current_player id
    # queries to get the current_player and dealer hand
    player_hand_query = (
        db.query(CardPlayed.card_rank, CardPlayed.card_suite)
        .filter(
            CardPlayed.lobby_id == lobby_id,
            CardPlayed.lobby_turn == turn,
            CardPlayed.entity == "Player",
        )
        .all()
    )
    if not player_hand_query:
        raise HTTPException(status_code=404, detail="Player hand not found")
    player_hand = [
        (card_rank, card_suite) for card_rank, card_suite in player_hand_query
    ]

    dealer_hand_query = (
        db.query(CardPlayed.card_rank, CardPlayed.card_suite)
        .filter(
            CardPlayed.lobby_id == lobby_id,
            CardPlayed.lobby_turn == turn,
            CardPlayed.entity == "Dealer",
        )
        .all()
    )
    if not dealer_hand_query:
        raise HTTPException(status_code=404, detail="Dealer hand not found")
    dealer_hand = [
        (card_rank, card_suite) for card_rank, card_suite in dealer_hand_query
    ]

    try:
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

        # update the database
        current_PlayerMove = (
            db.query(PlayerMove)
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.lobby_turn == turn)
            .first()
        )
        current_player = db.query(Player).filter(Player.id == player_id).first()
        ante_amount = current_PlayerMove.amount
        if outcome == "player_win":
            current_player.balance += 2 * ante_amount
            current_PlayerMove.winner = "Player"
        elif outcome == "tie":
            current_player.balance += 2 * ante_amount
            current_PlayerMove.winner = "tie"
        else:
            current_PlayerMove.winner = "Dealer"
        current_PlayerMove.move_type = "play"

        # commit changes to database
        db.commit()

        # get new player balance
        updated_player_balance = (
            db.query(Player.balance).filter(Player.id == player_id).first()
        )
        (player_balance,) = updated_player_balance

        # output to frontend
        return {"outcome": outcome, "balance": player_balance}

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )


@app.post("/fold")
async def fold(lobby_id: int, turn: int):
    try:
        # Get the player by ID
        current_player = (
            db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
        )
        if not current_player:
            raise HTTPException(status_code=404, detail="Host player not found")
        (player_id,) = current_player  # extract the current_player id

        current_PlayerMove = (
            db.query(PlayerMove)
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.lobby_turn == turn)
            .first()
        )
        if not current_PlayerMove:
            raise HTTPException(status_code=404, detail="PlayerMove not found")

        current_PlayerMove.move_type = "fold"
        current_PlayerMove.winner = "fold"
        db.commit()

        return {"outcome": "fold_commited"}

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )


@app.post("/exit")
async def exit(lobby_id: int):
    try:
        current_lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()

        if not current_lobby:
            raise HTTPException(status_code=404, detail="Lobby not found")

        # Update the lobby status directly
        current_lobby.status = "END"
        db.commit()

        return {"message": "Exited lobby"}

    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/get-stats")
async def get_Stats(player_id: int):
    try:
        result = db.execute(
            text("EXEC GetPlayerStats :player_id"), {"player_id": player_id}
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Player not found")

        # Extracting stats from result
        games_played = result.gamesplayed if result.gamesplayed else 0
        wins = result.wins if result.wins else 0
        defeats = result.defeats if result.defeats else 0
        plays = result.plays if result.plays else 0
        folds = result.folds if result.folds else 0

        # Calculating ratios
        win_ratio = wins / games_played if games_played > 0 else 0
        lose_ratio = defeats / games_played if games_played > 0 else 0
        play_ratio = plays / games_played if games_played > 0 else 0
        fold_ratio = folds / games_played if games_played > 0 else 0

        # Preparing the JSON response
        response = {
            "balance": result.balance,
            "createdAt": result.createdat,
            "gamesPlayed": games_played,
            "turnsPlayed": result.turnsplayed,
            "wins": wins,
            "defeats": defeats,
            "plays": plays,
            "folds": folds,
            "winRatio": win_ratio,
            "loseRatio": lose_ratio,
            "playRatio": play_ratio,
            "foldRatio": fold_ratio,
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/set-balance")
async def set_balance(player_id: int):
    # Check if player with given ID exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    # Set player balance to $1000
    player.balance = 1000.0
    db.commit()
    db.refresh(player)

    return {"setSuccess": True, "balance": player.balance}
