from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
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

class Rating(BaseModel):
    shoe_id: int
    user_id: int
    rating: int
    comment: str

@router.post("/shoes/:shoe_id/ratings/:rating_id")
def post_shoe_rating(Rating):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO ratings (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           JOIN shoes AS shoes_ratings ON ratings.shoe_id = shoes.shoe_id
                                           WHERE shoe_id = :shoe_id
                                           """),
                                        [{"shoe_id": Rating.shoe_id, "rating": Rating.rating, "rating": Rating.rating, "comment": Rating.comment}])
    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[User]):
    """ """
    print(wholesale_catalog)
  
    
    return plan