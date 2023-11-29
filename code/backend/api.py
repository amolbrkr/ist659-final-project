import os
import hashlib
from models.models import Player, Lobby, CardPlayed, PlayerMove
from models.request_models import PlayerCreate, PlayerLogin
from models.functions import create_deck, rank_hand, update_player_balance, deal_hand
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, func
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
            turn=0
        )
        db.add(new_lobby)
        db.commit()

        new_lobby = db.query(Lobby).order_by(Lobby.id.desc()).first()
        return {
            "lobby.id": new_lobby.id,
            "lobby.turn": 0,
        }

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation
        if "duplicate key" in str(e):
            raise HTTPException(status_code=409, detail="Duplicate lobby creation")
        else:
            # Handle other database-related errors
            raise HTTPException(status_code=500, detail="Database error")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
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

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Something went wrong, error: {str(err)}"
        )

    finally:
        # Close the database connection
        db.close()




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
            turn=0
        )
        db.add(new_lobby)
        db.commit()

        new_lobby = db.query(Lobby).order_by(Lobby.id.desc()).first()
        return {
            "lobby.id": new_lobby.id,
            "lobby.turn": 0,
        }

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation
        if "duplicate key" in str(e):
            raise HTTPException(status_code=409, detail="Duplicate lobby creation")
        else:
            # Handle other database-related errors
            raise HTTPException(status_code=500, detail="Database error")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()

>>>>>>> e8cc3e04834b6a43a87f990fac1d811afa582792

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
            move_type='none',
            winner='none'
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
                entity='Player'
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
                entity='Dealer'
            )
            db.add(dealer_CardPlayed)

        # commit all changes to the database
        db.commit()
        
        # return the info to the front end
        return {
            "lobby": lobby_id,
            "turn": new_turn,
            "lobby_hand": lobby_hand,
            "player_hand": player_hand,
        }

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()


db.close()


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
        current_PlayerMove = db.query(PlayerMove).filter(PlayerMove.lobby_id == lobby_id, PlayerMove.lobby_turn == turn).first()
        current_player = db.query(Player).filter(Player.id == player_id).first()
        ante_amount = current_PlayerMove.amount
        if outcome == "player_win":
            current_player.balance += 2 * ante_amount
            current_PlayerMove.winner = 'Player'
        elif outcome == "tie":
            current_player.balance += 2 * ante_amount
            current_PlayerMove.winner = 'tie'
        else:
            current_PlayerMove.winner = 'Dealer'
        current_PlayerMove.move_type = 'play'

        # commit changes to database
        db.commit()

        # get new player balance
        updated_player_balance = db.query(Player.balance).filter(Player.id == player_id).first()
        (player_balance,) = updated_player_balance

        # output to frontend
        return {"outcome": outcome,
                "balance": player_balance}

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()

@app.post("/fold")
async def fold(lobby_id: int, turn: int):
    try:
        # Get the player by ID
        current_player = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
        if not current_player:
            raise HTTPException(status_code=404, detail="Host player not found")
        (player_id,) = current_player  # extract the current_player id

        current_PlayerMove = db.query(PlayerMove).filter(PlayerMove.lobby_id == lobby_id, PlayerMove.lobby_turn == turn).first()
        if not current_PlayerMove:
            raise HTTPException(status_code=404, detail="PlayerMove not found")

        current_PlayerMove.move_type = 'fold'
        current_PlayerMove.winner = 'fold'
        db.commit()

        # Close the database connection
        db.close()

        return {"outcome": "fold_commited"}

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()


@app.post("/exit")

async def exit_lobby(lobby_id: int):
    try:
        # when exiting the lobby, we update the statistics in the player table
        current_player = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
        if not current_player:
            raise HTTPException(status_code=404, detail="Host player not found")
        (player_id,) = current_player  # extract the current_player id

        player_stats = db.query(Player).filter(Player.id == player_id).first()
        if not player_stats:
            raise HTTPException(status_code=404, detail="Player statistics not found")


        player_stats.gamesPlayed = db.query(func.count('*')).select_from(Lobby).filter(Lobby.hostPlayerId == player_id).scalar()
        db.commit()

        # Close the database connection
        db.close()

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()

        # Update games played
        player_stats.gamesPlayed = db.query(func.count(Lobby.id)).filter(Lobby.hostPlayerId == player_id).scalar()


async def exit(lobby_id: int):
    # when exiting the lobby we update the statistics in the player table
    current_player = db.query(Lobby.hostPlayerId).filter(Lobby.id == lobby_id).first()
    if not current_player:
        raise HTTPException(status_code=404, detail="Host player not found")
    (player_id,) = current_player  # extract the current_player id
    player_stats = db.query(Player).filter(Player.id == player_id).first()

    try:
        # Update games played
        player_stats.gamesPlayed = (
            db.query(func.count(Lobby.id)).filter(Lobby.hostPlayerId == player_id).scalar()
        )

        # Update turns played
        player_stats.turnsPlayed = (
            db.query(func.sum(Lobby.turn)).filter(Lobby.hostPlayerId == player_id).scalar()
        )

        # Calculate turns per game ratio
        if player_stats.gamesPlayed > 0:  # Avoid division by zero
            player_stats.turnsPerGame = player_stats.turnsPlayed / player_stats.gamesPlayed

        # Update wins
        player_stats.wins += (
            db.query(func.count(PlayerMove.id))
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.winner == "Player")
            .scalar()
        )

        # update losses
        player_stats.defeats += (
            db.query(func.count(PlayerMove.id))
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.winner == "Dealer")
            .scalar()
        )

        # update plays
        player_stats.plays += (
            db.query(func.count(PlayerMove.id))
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.move_type == "play")
            .scalar()
        )

        # update plays
        player_stats.folds += (
            db.query(func.count(PlayerMove.id))
            .filter(PlayerMove.lobby_id == lobby_id, PlayerMove.move_type == "fold")
            .scalar()
        )

        # Update turns played
        player_stats.turnsPlayed = db.query(func.sum(Lobby.turn)).filter(Lobby.hostPlayerId == player_id).scalar()

        # Calculate turns per game ratio
        if player_stats.gamesPlayed > 0:  # Avoid division by zero
            player_stats.turnsPerGame = player_stats.turnsPlayed / player_stats.gamesPlayed

        # Update wins
        player_stats.wins += db.query(func.count(PlayerMove.id)).filter(
            PlayerMove.lobby_id == lobby_id,
            PlayerMove.winner == 'Player'
        ).scalar()

        # Update defeats
        player_stats.defeats += db.query(func.count(PlayerMove.id)).filter(
            PlayerMove.lobby_id == lobby_id,
            PlayerMove.winner == 'Dealer'
        ).scalar()

        # Calculate win ratio if games played is more than zero
        if player_stats.gamesPlayed > 0:
            player_stats.winRatio = player_stats.wins / player_stats.gamesPlayed

        # Calculate play ratio if games played is more than zero
        if player_stats.gamesPlayed > 0:
            player_stats.playRatio = player_stats.plays / player_stats.gamesPlayed

        # Calculate fold ratio if games played is more than zero
        if player_stats.gamesPlayed > 0:
            player_stats.foldRatio = player_stats.folds / player_stats.gamesPlayed

        db.commit()

        return {"message": "Player stats updated successfully"}

    except IntegrityError as e:
        # Check if the error is related to a unique constraint violation or other database-related issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as err:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Something went wrong, error: {str(err)}")

    finally:
        # Close the database connection
        db.close()

    return {"message": "Player stats updated successfully"}
