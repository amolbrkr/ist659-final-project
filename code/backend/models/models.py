from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Card(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True, nullable=False)
    card_value = Column(String(2), nullable=False)
    card_suit = Column(String(50), nullable=False)

class Player(Base):
    __tablename__ = 'player'
    player_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    player_fName = Column(String(50), nullable=False)
    player_lName = Column(String(50), nullable=False)
    player_email = Column(String(50), unique=True, nullable=False)
    player_userName = Column(String(50), unique=True, nullable=False)
    player_money = Column(Numeric(10,2))
    player_createdAt = Column(Date, nullable=False)

class PStats(Base):
    __tablename__ = 'pStats'
    pStats_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pStats_wins = Column(Integer)
    pStats_defeats = Column(Integer)
    pStats_winRatio = Column(Float)
    pStats_totMoney = Column(Numeric)
    pStats_winnings = Column(Numeric)
    pStats_losses = Column(Numeric)
    pStats_royalFlush = Column(Integer)
    pStats_bestHand = Column(String, nullable=False)

class Match(Base):
    __tablename__ = 'match'
    match_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    match_ante = Column(Numeric)
    match_smallBlind = Column(Numeric, nullable=False)
    match_bigBlind = Column(Numeric, nullable=False)
    match_maxBet = Column(Numeric)
    match_player1 = Column(String, nullable=False)
    match_player2 = Column(String, nullable=False)
    match_player3 = Column(String)
    match_player4 = Column(String)
    match_player5 = Column(String)
    match_winner = Column(String, nullable=False)
    match_date = Column(Date, nullable=False)

class Lobby(Base):
    __tablename__ = 'lobby'
    lobby_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    lobby_player1 = Column(String, nullable=False)
    lobby_player2 = Column(String, nullable=False)
    lobby_player3 = Column(String)
    lobby_player4 = Column(String)
    lobby_player5 = Column(String)

class MatchDet(Base):
    __tablename__ = 'matchDet'
    matchDet_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    matchDet_turn = Column(String, nullable=False)
    matchDet_player1Move = Column(String, nullable=False)
    matchDet_player1HoleCard1 = Column(Integer, nullable=False)
    matchDet_player1HoleCard2 = Column(Integer, nullable=False)
    matchDet_player2Move = Column(String, nullable=False)
    matchDet_player2HoleCard1 = Column(Integer, nullable=False)
    matchDet_player2HoleCard2 = Column(Integer, nullable=False)
    matchDet_player3Move = Column(String, nullable=False)
    matchDet_player3HoleCard1 = Column(Integer, nullable=False)
    matchDet_player3HoleCard2 = Column(Integer, nullable=False)
    matchDet_player4Move = Column(String, nullable=False)
    matchDet_player4HoleCard1 = Column(Integer, nullable=False)
    matchDet_player4HoleCard2 = Column(Integer, nullable=False)
    matchDet_player5Move = Column(String, nullable=False)
    matchDet_player5HoleCard1 = Column(Integer, nullable=False)
    matchDet_player5HoleCard2 = Column(Integer, nullable=False)
    matchDet_flopCard1 = Column(Integer, nullable=False)
    matchDet_flopCard2 = Column(Integer, nullable=False)
    matchDet_flopCard3 = Column(Integer, nullable=False)
    matchDet_turnCard = Column(Integer, nullable=False)
    matchDet_riverCard = Column(Integer, nullable=False)


class Login(Base):
    __tablename__ = 'login'
    login_username = Column(String, primary_key=True, nullable=False)
    login_password = Column(String, nullable=False)