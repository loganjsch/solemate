from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    # Can return a max of 20 items.
    catalog = []

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("""
                                                     SELECT sku, SUM(potion_ledger.potion_change) AS inventory, price, potion_type
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