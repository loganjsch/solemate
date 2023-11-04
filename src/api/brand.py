from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/brands",
    tags=["brands"],
    dependencies=[Depends(auth.get_api_key)],
)

class Shoe(BaseModel):
    shoe_id: int
    name: str
    brand: str
    price: int
    color: str
    material: str
    tags: list[str]
    type: str

class ShoeCompany(BaseModel):
    brand_name: str
    email: str
    pasword: str
    shoes: list[Shoe]

@router.post("/{brand_id}/shoes")
def post_shoe(name: str, brand: str, price: int, color: str, material: str, tags: list[str], type: str):
    """Add new shoe to the app"""
    print(name, brand, price, color, material, tags, type)
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO shoes (name, brand, price, color, material, tags, type)
            VALUES (:name, :brand, :price, :color, :material, :tags, :type)
        """), {"name": name, "brand": brand, "price": price, "color": color, "material": material, "tags": tags, "type": type})

        return "OK"

@router.post("/")
def create_brand(brand_name: str, email: str, password: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO brands (brand_name, email, password) 
                                           VALUES (:brand_name, :email, :password)
                                           """),
                                        [{"brand_name": brand_name, "email": email, "password": password}])
    return "OK"