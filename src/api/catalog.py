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
                                                SELECT SUM(rating)
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

<<<<<<< HEAD
=======
@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    # Can return a max of 20 items.
    catalog = []

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("""
                                                     SELECT sku, AVG(potion_ledger.potion_change) AS inventory, price, potion_type
                                                     FROM potions
                                                     JOIN potion_ledger ON potion_ledger.potion_id = potions.id
                                                     GROUP BY potions.id
                                                     """))
    for row in result:
        if(row.inventory > 0):
            catalog.append(
                {
                    "sku": row.sku,
                    "name": row.sku,
                    "quantity": row.inventory,
                    "price": row.price,
                    "potion_type": row.potion_type,
                }
            )

    return catalog
>>>>>>> 97e531b215a15ed4bdf6b404f1f55cd69e2bc2fa
