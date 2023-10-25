from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/inventory")
def get_inventory():
    """ """
    with db.engine.begin() as connection:
        gold = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(gold_change) AS gold
                                                  FROM gold_ledger
                                                  """)).scalar_one()
        red = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(red_ml_change) AS red
                                                  FROM ml_ledger
                                                  """)).scalar_one()
        green = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(green_ml_change) AS green
                                                  FROM ml_ledger
                                                  """)).scalar_one()
        blue = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(blue_ml_change) AS blue
                                                  FROM ml_ledger
                                                  """)).scalar_one()
        dark = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(dark_ml_change) AS dark
                                                  FROM ml_ledger
                                                  """)).scalar_one()
        tot_pots = connection.execute(sqlalchemy.text("""
                                                      SELECT SUM(potion_change) AS inventory
                                                      FROM potion_ledger
                                                      """)).scalar_one()

    tot_ml = red + green + blue + dark   
    return {"number_of_potions": tot_pots, "ml_in_barrels": tot_ml, "gold": gold}

class Result(BaseModel):
    gold_match: bool
    barrels_match: bool
    potions_match: bool

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"
