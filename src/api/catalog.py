from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/shoes")
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