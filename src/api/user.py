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

@router.post("/{user_id}/{shoe_id}")
def add_shoe_to_Collection(shoe_id: int, user_id: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO shoes_to_users (shoe_id, user_id) 
                                           VALUES (:shoe_id, :user_id)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id}])
    return "OK"

@router.get("/{user_id}/reviews")
def get_user_reviews(user_id: int):
    """ """
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text("""
                                                    SELECT shoe.name, rating, comment FROM ratings AS rating
                                                    JOIN shoes AS shoe ON shoe.shoe_id = rating.shoe_id
                                                    WHERE rating.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
    ratings = []
    for review in reviews:
        ratings.append(
                    {
                    "shoe_name": review.name,
                    "rating": review.rating,
                    "comment": review.comment
                    }
                    )
    
    return ratings

@router.put("/{user_id}/shoes")
def get_user_collection(user_id: int):
    """ """
    with db.engine.begin() as connection:
        collection = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT name, rating, comment FROM shoes
                                                    JOIN shoes_to_users AS join_table ON join_table.shoe_id = shoes.shoe_id
                                                    WHERE join_table.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
        
    shoes = []

    for shoe in collection:
        shoes.append(
                {
                "shoe_name": shoe.name
                }
        )
    return shoes