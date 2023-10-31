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

    stats = relationship("PlayerStat", uselist=False, back_populates="player")

    def __init__(
        self, firstname, lastname, username, passwordHash, balance=100.0, createdAt=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.passwordHash = passwordHash
        self.balance = balance
        self.createdAt = createdAt if createdAt else datetime.utcnow()


class PlayerStat(Base):
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

    def __init__(
        self,
        id,
        wins,
        defeats,
        winRatio,
        totalMoney,
        winnings,
        losses,
        royalFlush,
        bestHand,
    ):
        self.id = id
        self.wins = wins
        self.defeats = defeats
        self.winRatio = winRatio
        self.totalMoney = totalMoney
        self.winnings = winnings
        self.losses = losses
        self.royalFlush = royalFlush
        self.bestHand = bestHand


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currentPlayers = Column(Integer, default=1, nullable=False)
    maxPlayers = Column(Integer, default=5, nullable=False)
    status = Column(String(50), default="WAITING", nullable=False)
    hostPlayerId = Column(Integer, ForeignKey("players.id"), nullable=False)
    turn = Column(Integer, default=0, nullable=False)

    def __init__(
        self,
        currentPlayers=1,
        maxPlayers=5,
        status="WAITING",
        hostPlayerId=None,
        turn=1,
    ):
        self.currentPlayers = currentPlayers
        self.maxPlayers = maxPlayers
        self.status = status
        self.hostPlayerId = hostPlayerId
        self.turn = turn


class PlayerLobby(Base):
    __tablename__ = "playerLobby"

    player_id = Column(
        Integer, ForeignKey("players.id"), primary_key=True, nullable=False
    )
    lobby_id = Column(
        Integer, ForeignKey("lobbies.id"), primary_key=True, nullable=False
    )

    def __init__(self, player_id, lobby_id):
        self.player_id = player_id
        self.lobby_id = lobby_id


class PlayerMove(Base):
    __tablename__ = "playerMoves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    move_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    move_time = Column(DateTime)

    def __init__(self, player_id, lobby_id, move_type, amount, move_time=None):
        self.player_id = player_id
        self.lobby_id = lobby_id
        self.move_type = move_type
        self.amount = amount
        self.move_time = move_time if move_time else datetime.utcnow()


class PlayerCard(Base):
    __tablename__ = "playerCards"

    player_id = Column(
        Integer, ForeignKey("players.id"), primary_key=True, nullable=False
    )
    lobby_id = Column(
        Integer, ForeignKey("lobbies.id"), primary_key=True, nullable=False
    )
    lobby_turn = Column(Integer, ForeignKey("lobbies.turn"), nullable=False)
    card_rank = Column(String(2), nullable=False)
    card_suite = Column(String(10), nullable=False)

    def __init__(self, player_id, lobby_id, lobby_turn, card_rank, card_suite):
        self.player_id = player_id
        self.lobby_id = lobby_id
        self.lobby_turn = lobby_turn
        self.card_rank = card_rank
        self.card_suite = card_suite


class DealerCard(Base):
    __tablename__ = "dealerCards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    lobby_turn = Column(Integer, ForeignKey("lobbies.turn"), nullable=False)
    card_rank = Column(String(2), nullable=False)
    card_suite = Column(String(10), nullable=False)

    def __init__(self, lobby_id, lobby_turn, card_rank, card_suite):
        self.lobby_id = lobby_id
        self.lobby_turn = lobby_turn
        self.card_rank = card_rank
        self.card_suite = card_suite


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    rank = Column(String(2))
    suit = Column(String(50))

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class Bid(Base):
    __tablename__ = "bids"

    bid_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    bid_type = Column(Enum("Ante", "Play", "Bonus"), nullable=False)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    bid_time = Column(DateTime, server_default=func.now())


class TurnCount(Base):
    __tablename__ = "turn_count"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, default=0)
