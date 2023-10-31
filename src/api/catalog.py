from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/shoes", tags=["shoes"])
def get_shoe_catalog():
    """ """
    with db.engine.begin() as connection:
        catalog = connection.execute(sqlalchemy.text("""SELECT * 
                                                     FROM shoes 
                                                     ORDER BY RANDOM() 
                                                     LIMIT 10"""))
    ret = []
    for shoe in catalog:
        with db.engine.begin() as connection:
            ave_rating = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT AVG(rating)
                                                FROM ratings
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe.shoe_id}]).scalar_one()
        ret.append(
            {
                "name": shoe.name,
                "brand": shoe.brand,
                "rating": ave_rating
            }
        )
    return ret
