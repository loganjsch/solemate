from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver")
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    """ """
    gold_paid = 0
    red_ml = 0
    green_ml = 0
    blue_ml = 0
    dark_ml = 0
    for barrel in barrels_delivered:
        gold_paid += barrel.price * barrel.quantity
        if(barrel.potion_type == [1,0,0,0]):
            red_ml += barrel.ml_per_barrel * barrel.quantity
        elif(barrel.potion_type == [0,1,0,0]):
            green_ml += barrel.ml_per_barrel * barrel.quantity
        elif(barrel.potion_type == [0,0,1,0]):
            blue_ml += barrel.ml_per_barrel * barrel.quantity
        elif(barrel.potion_type == [0,0,0,1]):
            dark_ml += barrel.ml_per_barrel * barrel.quantity
        else:
            raise Exception('Invalid potion type')
    
    print(f"gold paid: {gold_paid} red_ml: {red_ml} blue_ml: {blue_ml} green_ml: {green_ml} dark_ml: {dark_ml}")
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO gold_ledger (gold_change) 
                                           VALUES (:gold_paid)
                                           """),
                                        [{"gold_paid": -gold_paid}])
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO ml_ledger (red_ml_change, green_ml_change, blue_ml_change, dark_ml_change) 
                                           VALUES (:red_ml, :green_ml, :blue_ml, :dark_ml)
                                           """),
                                        [{"red_ml": red_ml, "green_ml": green_ml,"blue_ml": blue_ml,"dark_ml": dark_ml}])
    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)
  
    with db.engine.begin() as connection:
        gold = connection.execute(sqlalchemy.text("""
                                                  SELECT SUM(gold_change)
                                                  FROM gold_ledger
                                                  """)).scalar_one()
    curr_gold = gold
    plan = []
    times = 0
    quants = {}
    lst = wholesale_catalog
    for barrel in wholesale_catalog:
        quants[barrel.sku] = 0

    
    while(curr_gold > 99 and times < 10):
        times += 1
        for barrel in wholesale_catalog:
            if(curr_gold >= barrel.price):
                if('LARGE' in barrel.sku or 'SMALL' in barrel.sku or "DARK" in barrel.sku):
                        quants[barrel.sku] += 1
                        curr_gold -= barrel.price
                        barrel.quantity -= 1
    
    for barrel in wholesale_catalog:
        if(quants[barrel.sku] != 0):
            plan.append(
                {
                    "sku": barrel.sku,
                    "quantity": quants[barrel.sku]
                }
            )
    
    return plan