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

# set directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(script_directory))))


DATABASE_URL = "sqlite:///database/poker"  # Replace with your database URL
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
