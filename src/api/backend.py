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

class Rating(BaseModel):
    shoe_id: int
    user_id: int
    rating: int
    comment: str

@router.get("")
def get_shoe_catalog():
    """ """
    with db.engine.begin() as connection:
        catalog = connection.execute(sqlalchemy.text("SELECT * FROM shoes"))
    ret = []
    for shoe in catalog:
        ret.append(
            {
                "shoe_id": shoe.shoe_id,
                "name": shoe.name,
                "brand": shoe.brand,
                "price": shoe.price,
                "colors": shoe.colors,
                "material": shoe.material,
                "tags": shoe.tags,
            }
        )
    return ret

@router.post("/{shoe_id}/ratings/{rating_id}")
def post_shoe_rating(Rating):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO ratings (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           """),
                                        [{"shoe_id": Rating.shoe_id, "rating": Rating.rating, "rating": Rating.rating, "comment": Rating.comment}])
    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[User]):
    """ """
    print(wholesale_catalog)
  
    
    return plan
