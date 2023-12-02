from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(50), unique=True)
    passwordHash = Column(String(100))
    balance = Column(Float, default=100)
    createdAt = Column(DateTime, default=datetime.utcnow)
    gamesPlayed = Column(Integer, default=0)
    turnsPlayed = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    defeats = Column(Integer, default=0)
    plays = Column(Integer, default=0)
    folds = Column(Integer, default=0)

    def __init__(
        self,
        firstname,
        lastname,
        username,
        passwordHash,
        balance=100.0,
        createdAt=None,
        gamesPlayed=0,
        turnsPlayed=0,
        wins=0,
        defeats=0,
        plays=0,
        folds=0,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.passwordHash = passwordHash
        self.balance = balance
        self.createdAt = createdAt if createdAt else datetime.utcnow()
        self.gamesPlayed = gamesPlayed
        self.turnsPlayed = turnsPlayed
        self.wins = wins
        self.defeats = defeats
        self.plays = plays
        self.folds = folds


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), default="WAITING", nullable=False)
    hostPlayerId = Column(Integer, ForeignKey("players.id"), nullable=False)
    turn = Column(Integer, default=0, nullable=False)

    def __init__(
        self,
        status="WAITING",
        hostPlayerId=None,
        turn=0,
    ):
        self.status = status
        self.hostPlayerId = hostPlayerId
        self.turn = turn


class PlayerMove(Base):
    __tablename__ = "playerMoves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    lobby_turn = Column(Integer, nullable=False, default=1)
    move_type = Column(String(4), nullable=False)
    amount = Column(Float, nullable=False)
    winner = Column(String(6), nullable=False, default="none")
    move_time = Column(DateTime)

    def __init__(self, lobby_id, move_type, amount, winner, lobby_turn, move_time=None):
        self.lobby_id = lobby_id
        self.lobby_turn = lobby_turn
        self.move_type = move_type
        self.amount = amount
        self.winner = winner
        self.move_time = move_time if move_time else datetime.utcnow()


class CardPlayed(Base):
    __tablename__ = "CardsPlayed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    lobby_turn = Column(Integer, nullable=False)
    card_rank = Column(String(2), nullable=False)
    card_suite = Column(String(10), nullable=False)
    entity = Column(String(6), nullable=False)

    def __init__(self, lobby_id, lobby_turn, card_rank, card_suite, entity):
        self.lobby_id = lobby_id
        self.lobby_turn = lobby_turn
        self.card_rank = card_rank
        self.card_suite = card_suite
        self.entity = entity
