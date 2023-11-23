from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/prizes",
    tags=["prizes"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("")
def get_prizes():
    """Returns list of all available prizes"""
    
    with db.engine.begin() as connection:

        prizes = connection.execute(sqlalchemy.text("""
                                            SELECT prize_ledger.shoe_id,COALESCE(SUM(change),0) as quantity,price,name,brand
                                            FROM prize_ledger
                                            JOIN shoes ON prize_ledger.shoe_id = shoes.shoe_id
                                            GROUP BY prize_ledger.shoe_id,price,name,brand
                                            HAVING COALESCE(SUM(change),0) > 0
                                            ORDER BY price ASC
                                           """))

        ret = []

        for prize in prizes:
            ret.append(
                {
                    "shoe_id": prize.shoe_id,
                    "shoe_brand":prize.brand,
                    "shoe_name":prize.name,
                    "quantity":prize.quantity,
                    "point_cost":prize.price * 50
                }
            )

        return ret
    
@router.post("/cart/{user_id}")
def create_cart(user_id: int):
    """ """
    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("""INSERT INTO prize_carts (user_id)
                                            VALUES (:user_id)
                                            RETURNING cart_id"""),
                                            [{"user_id":user_id}]).scalar_one()

    
    return {"cart_id": id}

@router.post("/carts/{cart_id}/add")
def set_item_quantity(cart_id: int, shoe_id:int,quantity:int):
    """ """
    try:
        with db.engine.begin() as connection:

            prizes = connection.execute(sqlalchemy.text(""" 
                                                WITH prizes AS (
                                                    SELECT prize_ledger.shoe_id,COALESCE(SUM(change),0) as quantity,price,name,brand
                                                    FROM prize_ledger
                                                    JOIN shoes ON prize_ledger.shoe_id = shoes.shoe_id
                                                    GROUP BY prize_ledger.shoe_id,price,name,brand
                                                )
                                                SELECT * FROM prizes
                                                WHERE prizes.shoe_id  = :shoe_id AND prizes.quantity > 0
                                            """),[{"shoe_id":shoe_id}]).first()
            if not prizes:
                raise Exception ("ERROR: Invalid shoe_id")
            
            if prizes.quantity < quantity:
                raise Exception ("ERROR: quantity higher than inventory")
            
            if quantity < 1:
                raise Exception ("ERROR: quantity cannot be less than 1")


            connection.execute(sqlalchemy.text("""INSERT INTO prize_cart_items (cart_id,shoe_id,quantity)
                                                VALUES( :cart_id,:shoe_id, :quantity)"""),
                                                [{"cart_id":cart_id,"quantity":quantity,"shoe_id":shoe_id}])
    except Exception as error:
        return(f"Error returned: <<<{error}>>>")

    return "OK"


@router.post("carts/{cart_id}/checkout")
def checkout(cart_id: int):

    try:
        with db.engine.begin() as connection:

            active = connection.execute(sqlalchemy.text(""" SELECT active
                                                    FROM prize_carts
                                                    WHERE cart_id = :cart_id
                                                """),
                                                [{"cart_id":cart_id}]).scalar_one()

            if active is False:
                raise Exception("Error: Cart has already checked out")

            user_id  = connection.execute(sqlalchemy.text("""
                SELECT user_id
                FROM prize_carts
                WHERE cart_id = :cart_id
                """),
                [{"cart_id": cart_id}]).scalar_one()
            
            ###Authentication
            response = connection.execute(sqlalchemy.text("""
                                                SELECT is_logged_in
                                                FROM users
                                                WHERE user_id = :user_id
                                            """),
                                            [{"user_id": user_id}]).scalar_one()
            
            if response != True:
                raise Exception ("Login to Access this feature")
            #####

            total_cost = connection.execute(sqlalchemy.text(""" 
                SELECT SUM(50 * prize_cart_items.quantity * shoes.price)
                FROM prize_cart_items
                JOIN shoes on prize_cart_items.shoe_id = shoes.shoe_id
                WHERE cart_id = :cart_id"""),
                [{"cart_id":cart_id}]).scalar_one()
            
            points_available = connection.execute(sqlalchemy.text("""
                SELECT COALESCE(SUM(point_change),0)
                FROM point_ledger
                WHERE user_id = :user_id
                """),
                [{"user_id": user_id}]).scalar_one()
            
            if points_available < total_cost:
                raise  Exception("ERROR: Not enough points")
            
            total_items = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity)
                                                    FROM prize_cart_items
                                                    WHERE cart_id = :cart_id
                                                """),
                                                [{"cart_id":cart_id}]).scalar_one()
            
            connection.execute(sqlalchemy.text("""INSERT INTO point_ledger (user_id,point_change)
                                        VALUES (:user_id,-:total_cost)
                                        """),
                                        [{"total_cost":total_cost,"user_id":user_id}])
            
            connection.execute(sqlalchemy.text("""INSERT INTO orders (user_id,shoe_id,quantity)
                                                SELECT :user_id,prize_cart_items.shoe_id,prize_cart_items.quantity
                                                FROM prize_cart_items
                                                WHERE cart_id = :cart_id
                                                """),
                                                [{"cart_id":cart_id,"user_id":user_id}])
            
            connection.execute(sqlalchemy.text("""INSERT INTO prize_ledger (shoe_id,change)
                                                SELECT prize_cart_items.shoe_id,(prize_cart_items.quantity * -1)
                                                FROM prize_cart_items
                                                WHERE cart_id = :cart_id
                                                """),
                                                [{"cart_id":cart_id,"user_id":user_id}])
            
            connection.execute(sqlalchemy.text(""" UPDATE prize_carts
                                                    SET active = FALSE
                                                    WHERE cart_id = :cart_id
                                                """),
                                                [{"cart_id":cart_id}])
    except Exception as error:
        return(f"Error returned: <<<{error}>>>")
    


    return {"shoes_bought": total_items, "points_spent": total_cost}