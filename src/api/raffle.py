from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/raffle",
    tags=["raffle"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/points/{user_id}")
def get_points(user_id: int):
    """Retrieve total points for a user"""
    
    with db.engine.begin() as connection:

        ###Authentication
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM users
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": user_id}]).scalar_one()
        
        if response != True:
            return "Login to Access this feature"
        #####
        
        points = connection.execute(sqlalchemy.text("""
                                            SELECT COALESCE(SUM(point_change),0)
                                            FROM point_ledger
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": user_id}]).scalar_one()


        return "TOTAL POINTS: " + str(points)
    

@router.get("")
def get_raffles():
    """Returns list of all available raffles"""
    
    with db.engine.begin() as connection:

        raffles = connection.execute(sqlalchemy.text("""
                                            SELECT raffle_id,raffles.shoe_id,price,name,brand,start_time
                                            FROM raffles
                                            JOIN shoes ON raffles.shoe_id = shoes.shoe_id
                                            WHERE active = TRUE
                                            ORDER BY start_time ASC
                                           """))

        ret = []

        for raffle in raffles:
            ret.append(
                {   
                    "raffle_id": raffle.raffle_id,
                    "shoe_id": raffle.shoe_id,
                    "shoe_brand":raffle.brand,
                    "shoe_name":raffle.name,
                    "start_time":raffle.start_time.ctime(),
                    "entry_cost":raffle.price
                }
            )

        return ret
    
@router.get("/enter/{user_id}")
def enter_raffle(user_id:int,entries:int,raffle_id:int):
    """Enters user into raffle of their choosing"""
    
    with db.engine.begin() as connection:

        ###Authentication
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM users
                                            WHERE user_id = :user_id
                                        """),
                                        [{"user_id": user_id}]).scalar_one()
        
        if response != True:
            return "Login to Access this feature"
        #####

        if entries < 1:
            return "ERROR: Entries cannot be less than 1"

        raffle = connection.execute(sqlalchemy.text("""
                                            SELECT price
                                            FROM raffles
                                            JOIN shoes ON raffles.shoe_id = shoes.shoe_id
                                            WHERE raffle_id = :raffle_id
                                           """),[{"raffle_id":raffle_id}]).first()
        
        if not raffle:
            return "ERROR: Invalid Raffle ID"
        
        points_available = connection.execute(sqlalchemy.text("""
                SELECT COALESCE(SUM(point_change),0)
                FROM point_ledger
                WHERE user_id = :user_id
                """),
                [{"user_id": user_id}]).scalar_one()
        
        if points_available < entries * raffle.price:
            return "ERROR: Insufficient Points"


        for i in range(entries):
            connection.execute(sqlalchemy.text
                ("""INSERT INTO raffle_entries (raffle_id,user_id)
                    VALUES(:raffle_id,:user_id)
                    """),
                [{"raffle_id":raffle_id,"user_id":user_id}])
            

        return "Raffle Entry Sucessful"