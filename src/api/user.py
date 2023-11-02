from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_id: int
    name: str
    username: str
    email: str
    password: str

@router.post("/{name}")
def create_user(name: str, username: str, email: int, password: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO users (name, username, email, password) 
                                           VALUES (:name, :username, :email, :password)
                                           """),
                                        [{"name": name, "username": username, "email": email, "password": password}])
    return "OK"
