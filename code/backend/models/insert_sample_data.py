from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from datetime import date




engine = create_engine('sqlite:///C:/Users/franc/poker')
Session = sessionmaker(bind=engine)
session = Session()


# Initialize Player objects
players_to_add = [
    Player(
        firstname='John',
        lastname='Doe',
        username='johndoe123',
        passwordHash='123456',
        balance=100000,
        createdAt=date.today()
    ),
    Player(
        firstname='Amol',
        lastname='Borkar',
        username='amol',
        passwordHash='123456',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Francisco',
        lastname='Franco',
        username='francisco',
        passwordHash='123456',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Yashawi',
        lastname='Pandey',
        username='yashawi',
        passwordHash='123456',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Caleb',
        lastname='Brown',
        username='caleb',
        passwordHash='123456',
        balance=1000000,
        createdAt=date.today()
    ),
    Player(
        firstname='Michael',
        lastname='DAmore',
        username='michael',
        passwordHash='123456',
        balance=1000000,
        createdAt=date.today()
    )
]

# Add players to the session
for player in players_to_add:
    session.add(player)

# Commit the transaction
session.commit()

# Query to fetch players
query_results = session.query(Player.id, Player.username).all()

# Print the results
print("List of players added:")
for id, username in query_results:
    print(f"ID: {id}, Username: {username}")