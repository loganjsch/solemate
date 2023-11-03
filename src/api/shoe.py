from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/shoes",
    tags=["shoes"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_id: int
    name: str
    username: str
    email: str
    password: str

class Shoe(BaseModel):
    shoe_id: int
    name: str
    brand: str
    price: int
    color: str
    material: str
    tags: list[str]
    type: str

class Rating(BaseModel):
    shoe_id: int
    user_id: int
    rating: int
    comment: str

@router.get("/{shoe_id}")
def get_shoe(shoe_id: int):
    """ """
    with db.engine.begin() as connection:
        shoe = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT * FROM shoes
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}]).first()
        ave_rating = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT AVG(rating)
                                                FROM reviews
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}]).scalar_one()
    return {
        "shoe_id": shoe.shoe_id,
        "name": shoe.name,
        "brand": shoe.brand,
        "price": shoe.price,
        "color": shoe.color,
        "material": shoe.material,
        "tags": shoe.tags,
        "type": shoe.type,
        "rating": ave_rating
        }

@router.get("/{shoe_id}/reviews")
def get_shoe_reviews(shoe_id: int):
    """ """
    reviews = []
    with db.engine.begin() as connection:
        review_list = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT * 
                                                FROM reviews
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}])
    for review in review_list:
        reviews.append(
                    {
                    "user_id": review.user_id,
                    "rating": review.rating,
                    "comment": review.comment
                    }
                    )
    return reviews

@router.post("/{shoe_id}/review")
def post_shoe_review(shoe_id: str, user_id: str, rating: int, comment: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO reviews (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id, "rating": rating, "comment": comment}])
    return "OK"
