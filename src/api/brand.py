from fastapi import APIRouter, Depends
from enum import Enum
from backend import Shoe
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class ShoeCompany(BaseModel):
    brand_name: str
    shoes: list[Shoe]

@router.post("/deliver")
def post_shoe(new_shoe: Shoe):
    """Add new shoe to the app"""
    print(new_shoe)
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO shoes (name, brand, price, color, material, tags, type)
            VALUES (:name, :brand, :price, :color, :material, :tags, :type)
        """), {"name": new_shoe.name, "brand": new_shoe.brand, "price": new_shoe.price, "color": new_shoe.color, "material": new_shoe.material, "tags": new_shoe.tags, "type": new_shoe.type})

        return "OK"

# Gets called 4 times a day
@router.post("/plan")
def get_plan():
    """
    Go from barrel to bottle.
    """

    with db.engine.begin() as connection:

        return