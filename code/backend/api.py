from models.models import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

# Define SQLAlchemy database connection
DATABASE_URL = "sqlite:///poker.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL)
db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# Initialize FastAPI
app = FastAPI()

# Create request models using Pydantic
class LobbyCreate(BaseModel):
    lobby_name: str

@app.post("/create-lobby/", response_model=Lobby)
async def create_lobby(lobby: LobbyCreate):

    try:
        # Create a new lobby in the database
        new_lobby = Lobby(**lobby.dict())
        db.add(new_lobby)
        db.commit()
        db.refresh(new_lobby)
        return new_lobby
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Lobby name already exists")
    finally:
        db.close()

