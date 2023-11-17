from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from sqlalchemy import or_


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
def create_user(name: str, username: str, email: str, password: str):
    """ """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO users (name, username, email, password) 
                                           VALUES (:name, :username, :email, :password)
                                           """),
                                        [{"name": name, "username": username, "email": email, "password": password}])
    return "OK"

@router.post("/{user_id}/shoes/{shoe_id}")
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
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text("""
                                                    SELECT shoe.name, rating, comment FROM reviews AS rating
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

@router.get("/{user_id}/shoes")
def get_user_collection(user_id: int):
    """ """
    with db.engine.begin() as connection:
        collection = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT shoes.shoe_id, name, brand, color, material, price FROM shoes
                                                    JOIN shoes_to_users AS join_table ON join_table.shoe_id = shoes.shoe_id
                                                    WHERE join_table.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
        
    shoes = []

    for shoe in collection:
        shoes.append(
                {
                "shoe_id": shoe.shoe_id,
                "shoe_name": shoe.name,
                "brand": shoe.brand,
                "color": shoe.color,
                "material": shoe.material,
                "price": shoe.price
                }
        )
    return shoes

@router.get("/search/", tags=["search"])
def search_users(
    search_value: str = "",
    search_page: str = ""
):
    
    limit = 30
    
    if search_page == "":
        search_page = 0
    else:
        search_page = int(search_page)

    stmt = (
        sqlalchemy.select(
            db.users.c.username,
            db.users.c.name

        )
        .offset(search_page)
        .limit(limit)
    )


    counting = (
        sqlalchemy.select(
            sqlalchemy.func.count().label("count")
        )
        .select_from(db.users)
    )

    stmt = stmt.where(or_(db.users.c.username.ilike(f"%{search_value}%"),db.users.c.name.ilike(f"%{search_value}%")))
    counting = counting.where(or_(db.users.c.username.ilike(f"%{search_value}%"),db.users.c.name.ilike(f"%{search_value}%")))

    with db.engine.connect() as conn:

        result = conn.execute(stmt)
        count = conn.execute(counting).scalar_one()

        json = []
        for row in result:
            json.append(
                {
                    "name":row.name,
                    "username": row.username
                }
            )

    
    #calculate search page here
    prev = ""
    next = ""

    if search_page-limit >= 0:
        prev = str(search_page-limit)

    if search_page+limit < count:
        next = str(search_page+limit)

    return {
        "previous": prev,
        "next": next, 
        "results": json
    }