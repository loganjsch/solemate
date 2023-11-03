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

@router.post("/")
def create_user(name: str, username: str, email: int, password: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO users (name, username, email, password) 
                                           VALUES (:name, :username, :email, :password)
                                           """),
                                        [{"name": name, "username": username, "email": email, "password": password}])
    return "OK"

@router.post("/{user_id}/shoes")
def addTo_user_Collection(shoe_id: int, user_id: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO shoes_to_users (shoe_id, user_id) 
                                           VALUES (:shoe_id, :user_id)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id}])
    return "OK"

@router.get("/{user_id}/reviews")
def get_users_reviews(user_id: int):
    reviews = []
    with db.engine.begin() as connection:
        review_list = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT * FROM reviews
                                                    WHERE user_id = :user_id
                                                    """), 
                                                    [{"user_id": user_id}])
    for review in review_list:
        reviews.append(
                    {
                    "shoe_id": review.shoe_id,
                    "rating": review.rating,
                    "comment": review.comment
                    }
                    )
    return reviews
