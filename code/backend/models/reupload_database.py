# code to upload the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *  # Make sure Base is imported from your models file

# Your existing database URL
DATABASE_URL = "sqlite:///database/poker"
engine = create_engine(DATABASE_URL, echo=True)

# Drop everything
Base.metadata.drop_all(engine)

# Recreate the schema
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

