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

@router.post("/{user_id}/shoes/{shoe_id}")
def addTo_user_Collection(shoe_id: int, user_id: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO shoes_to_users (shoe_id, user_id) 
                                           VALUES (:shoe_id, :user_id)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id}])
    return "OK"

@router.get("/users/{user_id}/ratings")
def get_users_ratings(user_id: int):
    ratings = []
    with db.engine.begin() as connection:
        rating_list = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT * FROM ratings
                                                    WHERE user_id = :user_id
                                                    """), 
                                                    [{"user_id": user_id}])
    for rating in rating_list:
        ratings.append(
                    {
                    "shoe_id": rating.shoe_id,
                    "rating": rating.rating,
                    "comment": rating.comment
                    }
                    )
    return ratings
