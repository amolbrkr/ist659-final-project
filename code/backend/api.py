from models.models import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import os

#set directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(script_directory)))

# Define SQLAlchemy database connection
DATABASE_URL = "sqlite:///database/poker"  # Replace with your database URL
engine = create_engine(DATABASE_URL)
db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# Initialize FastAPI
app = FastAPI()

# Create request models using Pydantic
class LobbyCreate(BaseModel):
    lobby_name: str

# Create request models using Pydantic
class PlayerCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    passwordHash: str

@app.post("/create-player")
async def create_player(player: PlayerCreate):
    try:
        # Create a new plater in the database
        new_user = Player(
            firstname=player.firstname,
            lastname=player.lastname,
            username=player.username,
            passwordHash=player.passwordHash
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Player name already exists")
    finally:
        db.close()
