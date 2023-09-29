from models import *
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

# Modify this path to your DB
db_uri = 'sqlite:///C:/Users/franc/poker'
engine = create_engine(db_uri)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


expected_table_names = ['cards', 'player', 'pStats', 'match', 'lobby', 'matchDet', 'login']

inspector = inspect(engine)

table_names = inspector.get_table_names()

missing_tables = [table_name for table_name in expected_table_names if table_name not in table_names]

if not missing_tables:
    print("All expected model tables exist in the database.")
else:
    print("The following tables are missing from the database:", missing_tables)

