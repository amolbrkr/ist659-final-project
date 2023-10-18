import os
import hashlib
from models.models import Player, Lobby, PlayerLobby
from models.request_models import PlayerCreate
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

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

@app.post("/deal-cars")
async def deal_cards(playerId: int, lobbyId: int):

