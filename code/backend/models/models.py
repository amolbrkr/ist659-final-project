from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

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

    stats = relationship("PlayerStats", uselist=False, back_populates="player")


class PlayerStats(Base):
    __tablename__ = "playerStats"

    id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    wins = Column(Integer)
    defeats = Column(Integer)
    winRatio = Column(Float)
    totalMoney = Column(Float)
    winnings = Column(Float)
    losses = Column(Float)
    royalFlush = Column(Integer)
    bestHand = Column(String)
    player = relationship("Player", back_populates="stats")


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currentPlayers = Column(Integer, nullable=False)
    maxPlayers = Column(Integer, default=5, nullable=False)
    status = Column(String(50), default="WAITING", nullable=False)
    hostPlayerId = Column(Integer, ForeignKey("players.id"), nullable=False)


class PlayerLobby(Base):
    __tablename__ = "playerLobby"

    player_id = Column(
        Integer, ForeignKey("players.id"), primary_key=True, nullable=False
    )
    lobby_id = Column(
        Integer, ForeignKey("lobbies.id"), primary_key=True, nullable=False
    )


class PlayerMoves(Base):
    __tablename__ = "playerMoves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    move_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    move_time = Column(DateTime)


class PlayerCards(Base):
    __tablename__ = "playerCards"

    player_id = Column(
        Integer, ForeignKey("players.id"), primary_key=True, nullable=False
    )
    lobby_id = Column(
        Integer, ForeignKey("lobbies.id"), primary_key=True, nullable=False
    )
    card_rank = Column(String(2), primary_key=True, nullable=False)
    card_suite = Column(String(10), primary_key=True, nullable=False)


class Cards(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    rank = Column(String(2))
    suit = Column(String(50))
