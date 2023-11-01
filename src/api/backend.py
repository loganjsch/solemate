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
    colors: str
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
                                                [{"shoe_id": shoe_id}]).scalar_one()
        ave_rating = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT SUM(rating)
                                                FROM ratings
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}]).scalar_one()
    return {
        "shoe_id": shoe.shoe_id,
        "name": shoe.name,
        "brand": shoe.brand,
        "price": shoe.price,
        "colors": shoe.colors,
        "material": shoe.material,
        "tags": shoe.tags,
        "type": shoe.type,
        "rating": ave_rating
        }

@router.get("/{shoe_id}/ratings")
def get_shoe(shoe_id: int):
    """ """
    ratings = []
    with db.engine.begin() as connection:
        rating_list = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT * 
                                                FROM ratings
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}])
    for rating in rating_list:
        ratings.append(
                    {
                    "user_id": rating.user_id,
                    "rating": rating.rating,
                    "comment": rating.comment
                    }
                    )
    return ratings

@router.post("/{shoe_id}/ratings/{user_id}")
def post_shoe_rating(shoe_id: str, user_id: str, rating: int, comment: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO ratings (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id, "rating": rating, "comment": comment}])
    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[User]):
    """ """
    print(wholesale_catalog)
  
    
    return 0
