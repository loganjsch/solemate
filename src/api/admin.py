from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           TRUNCATE cart_items, carts, gold_ledger, ml_ledger, potion_ledger
                                           """))
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO gold_ledger (gold_change)
                                           VALUES (100)
                                           """))
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO ml_ledger (red_ml_change, green_ml_change, blue_ml_change, dark_ml_change)
                                           VALUES (0, 0, 0, 0)
                                           """))
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO potions_ledger (potion_change, potion_id)
                                           SELECT 0, potions.id
                                           FROM potions
                                           GROUP BY potion_id
                                           """))
    
    return "OK"


@router.get("/shop_info/")
def get_shop_info():
    """ """

    # TODO: Change me!
    return {
        "shop_name": "Jitter Juice",
        "shop_owner": "Charles Moreno",
    }

