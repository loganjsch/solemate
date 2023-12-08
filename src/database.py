import os
import dotenv
import sqlalchemy
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)
metadata_obj = sqlalchemy.MetaData()
shoes = sqlalchemy.Table("shoes", metadata_obj, autoload_with = engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with = engine)
reviews = sqlalchemy.Table("reviews", metadata_obj, autoload_with = engine)