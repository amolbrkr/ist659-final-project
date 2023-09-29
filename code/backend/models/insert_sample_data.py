from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from datetime import date




engine = create_engine('sqlite:///C:/Users/franc/poker')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


# Initialize Player objects
players_to_add = [
    Player(
        firstname='John',
        lastname='Doe',
        username='johndoe123',
        passwordHash='some_hash_here',
        balance=100.50,
        createdAt=date.today()
    ),
    Player(
        firstname='Amol',
        lastname='Borkar',
        username='amol_unique',
        passwordHash='some_hash_here',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Francisco',
        lastname='Franco',
        username='francisco_unique',
        passwordHash='some_hash_here',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Yashawi',
        lastname='Pandey',
        username='yashawi_unique',
        passwordHash='some_hash_here',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Caleb',
        lastname='Brown',
        username='caleb_unique',
        passwordHash='some_hash_here',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Michael',
        lastname='DAmore',
        username='michael_unique',
        passwordHash='some_hash_here',
        balance=1000000,
        createdAt=date.today()
    )
]

# Add players to the session
for player in players_to_add:
    session.add(player)

# Commit the transaction
session.commit()