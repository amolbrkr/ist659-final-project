from models import *
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Date,
    Float,
    inspect,
)

# Modify this path to your DB
db_uri = "sqlite:///C:/Users/franc/poker"
engine = create_engine(db_uri)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Updating expected_table_names to your schema
expected_table_names = ["players", "playerStats", "lobbies", "playerLobby", "cards"]

# Initialize the inspector and grab the table names from the database
inspector = inspect(engine)
table_names = inspector.get_table_names()

# Checking if tables are missing
missing_tables = [
    table_name for table_name in expected_table_names if table_name not in table_names
]

# Finally, a message to our humble user
if not missing_tables:
    print("All expected model tables exist in the database.")
else:
    print(
        f"Anomaly detected! The following tables are missing from the database: {missing_tables}"
    )
