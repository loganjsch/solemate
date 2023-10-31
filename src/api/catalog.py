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
        ret.append(
            {
                "shoe_id": shoe.shoe_id,
                "name": shoe.name,
                "brand": shoe.brand,
                "price": shoe.price,
                "color": shoe.color,
                "material": shoe.material,
                "tags": shoe.tags,
            }
        )
    return ret

