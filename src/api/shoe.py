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
                                                SELECT shoes.shoe_id,name,brand,price,color,material,tags,type, AVG(rating) as avg
                                                FROM shoes
                                                JOIN reviews ON reviews.shoe_id = shoes.shoe_id
                                                WHERE shoes.shoe_id = :shoe_id
                                                GROUP BY shoes.shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}]).first()
        
    return {
        "shoe_id": shoe.shoe_id,
        "name": shoe.name,
        "brand": shoe.brand,
        "price": shoe.price,
        "color": shoe.color,
        "material": shoe.material,
        "tags": shoe.tags,
        "type": shoe.type,
        "rating": shoe.avg
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
    if rating > 5 or rating < 1:
        return "INVALID RATING (1-5 INCLUSIVE)"
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO reviews (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id, "rating": rating, "comment": comment}])
    return "OK"


@router.get("/compare/{shoe_id_1}/{shoe_id_2}")
def compare_shoes(shoe_id_1: int, shoe_id_2: int):
    """"""
    with db.engine.begin() as connection:
        shoe1 = connection.execute(sqlalchemy.text("""
            SELECT s.shoe_id, s.name, s.brand, s.price, AVG(r.rating) as avg_rating
            FROM shoes s
            LEFT JOIN reviews r ON r.shoe_id = s.shoe_id
            WHERE s.shoe_id = :shoe_id_1
            GROUP BY s.shoe_id, s.name, s.brand, s.price
        """), {"shoe_id_1": shoe_id_1}).fetchone()

        shoe2 = connection.execute(sqlalchemy.text("""
            SELECT s.shoe_id, s.name, s.brand, s.price, AVG(r.rating) as avg_rating
            FROM shoes s
            LEFT JOIN reviews r ON r.shoe_id = s.shoe_id
            WHERE s.shoe_id = :shoe_id_2
            GROUP BY s.shoe_id, s.name, s.brand, s.price
        """), {"shoe_id_2": shoe_id_2}).fetchone()

        response = {
            "shoe_ids":[shoe1.shoe_id, shoe2.shoe_id],
            "shoe_names": [shoe1.name, shoe2.name],
            "brands":[shoe1.brand, shoe2.brand],
            "retail_prices":[shoe1.price, shoe2.price],
            "ratings":[shoe1.avg_rating, shoe2.avg_rating]
        }

        return response
