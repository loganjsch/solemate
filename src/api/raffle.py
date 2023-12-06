from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/raffles",
    tags=["raffle"],
    dependencies=[Depends(auth.get_api_key)],
)    

@router.get("/")
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

        ret = [dict(raffle) for raffle in raffles] 
        return ret if ret else {"message": "No active raffles available"} 
    
@router.post("/{raffle_id}/{user_id}")
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
            raise HTTPException(status_code=401, detail="Login required to access this feature")
        #####

        if entries < 1:
            raise HTTPException(status_code=400, detail="Must have at least 1 entry!")

        raffle = connection.execute(sqlalchemy.text("""
                                            SELECT price
                                            FROM raffles
                                            JOIN shoes ON raffles.shoe_id = shoes.shoe_id
                                            WHERE raffle_id = :raffle_id
                                           """),[{"raffle_id":raffle_id}]).first()
        
        if not raffle:
            raise HTTPException(status_code=404, detail="Raffle ID not found")
        
        points_available = connection.execute(sqlalchemy.text("""
                SELECT COALESCE(SUM(point_change),0)
                FROM point_ledger
                WHERE user_id = :user_id
                """),
                [{"user_id": user_id}]).scalar_one()
        
        if points_available < entries * raffle.price:
            raise HTTPException(status_code=400, detail="Insufficient Points")

        connection.execute(sqlalchemy.text("""
                                           INSERT INTO point_ledger (user_id,point_change) 
                                           VALUES (:user_id,:point_change)
                                           """),
                                        [{"user_id": user_id,"point_change":-entries*raffle.price}])

        for i in range(entries):
            connection.execute(sqlalchemy.text
                ("""INSERT INTO raffle_entries (raffle_id,user_id)
                    VALUES(:raffle_id,:user_id)
                    """),
                [{"raffle_id":raffle_id,"user_id":user_id}])
            

        return "Raffle Entry Sucessful"