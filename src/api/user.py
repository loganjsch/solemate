import base64
import os
import dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from sqlalchemy import or_
from cryptography.fernet import Fernet
import re


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    address: str

@router.post("/")
def create_user(user:User):
    """ """

    #check if password long enough
    if len(user.password) < 8:
        return "Password must be atleast 8 characters"

    #check for valid email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(not re.fullmatch(regex, user.email)):
        return("Invalid Email")

    #add salt & encrypt password before insertion
    dotenv.load_dotenv()
    crypto_key = bytes(os.environ.get("CRYPTO_KEY"),'utf-8')

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(crypto_key))
    f = Fernet(key)

    user.password = f.encrypt(bytes(user.password,'utf-8'))

    with db.engine.begin() as connection:
        #check if username already in use
        validUser = connection.execute(sqlalchemy.text("""
                                                SELECT username FROM users
                                                WHERE username = :username
                                            """),
                                            [{"username": user.username}]).all()
        
        if len(validUser) > 0:
            return "Username Already In Use. Pick Another Username"
        
        #check if email already in use
        validEmail = connection.execute(sqlalchemy.text("""
                                                SELECT email FROM users
                                                WHERE email = :email
                                            """),
                                            [{"email": user.email}]).all()
        
        if len(validEmail) > 0:
            return "Email Already In Use. Use Another Email"

        #insert user info into users table
        try:
            user_id = connection.execute(sqlalchemy.text("""
                                                INSERT INTO users (name, username, email, password,salt,address) 
                                                VALUES (:name, :username, :email, :password,:salt,:address),
                                                RETURNING id
                                            """),
                                            [{"name": user.name, "username": user.username, "email": user.email, "password": user.password,"salt":salt,"address":user.address}]).scalar_one()
        except Exception:
            print("Couldn't Create Account")
            
    return "Account" + user_id + " Successfully Created. Please Login to Continue."

@router.post("/login")
def login(username: str, password: str):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
                                            SELECT password,salt
                                            FROM users
                                            WHERE username = :username
                                           """),
                                        [{"username": username}]).first()
    
        if not response:
            return "Invalid Username"
        
        #Get key for decyption
        dotenv.load_dotenv()
        crypto_key = bytes(os.environ.get("CRYPTO_KEY"),'utf-8')
        
        #get user values from database
        pw = bytes(response.password)
        salt = bytes(response.salt)

        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(crypto_key))
        f = Fernet(key)
        token = f.decrypt(pw)

        if token == bytes(password,'utf-8'):
            connection.execute(sqlalchemy.text("""
                                            UPDATE users
                                            SET is_logged_in = TRUE
                                            WHERE username = :username
                                           """),
                                        [{"username": username}])

            return "Logged In"
        else:
            return "Incorrect Password"

@router.post("/{user_id}/logout")
def logout(user_id:int):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM users
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": user_id}]).scalar_one()
        
        if response != True:
            return "Cannot Logout"
        
        connection.execute(sqlalchemy.text("""
                                            UPDATE users
                                            SET is_logged_in = FALSE
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": user_id}])

        return "Logged Out"
        
@router.post("/{user_id}/delete")
def delete(user_id: str):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
            SELECT username
            FROM users
            WHERE user_id = :user_id
            """), {"user_id": user_id}).first()

        if not response:
            return "Invalid User"
        
        connection.execute(sqlalchemy.text("""
            DELETE FROM users
            WHERE user_id = :user_id
        """
        ), {"user_id": user_id})

    return "Account Deleted"

@router.post("/{user_id}/shoes/{shoe_id}")
def add_shoe_to_Collection(shoe_id: int, user_id: int):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM users
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": user_id}]).scalar_one()
        
        if response != True:
            return "Login to Access this feature"


        connection.execute(sqlalchemy.text("""
                                           INSERT INTO shoes_to_users (shoe_id, user_id) 
                                           VALUES (:shoe_id, :user_id)
                                           """),
                                        [{"shoe_id": shoe_id, "user_id": user_id}])
    return "Sucessfully Added"

@router.get("/{user_id}/reviews")
def get_user_reviews(user_id: int):
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text("""
                                                    SELECT shoe.name, rating, comment FROM reviews AS rating
                                                    JOIN shoes AS shoe ON shoe.shoe_id = rating.shoe_id
                                                    WHERE rating.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
    ratings = []
    for review in reviews:
        ratings.append(
                    {
                    "shoe_name": review.name,
                    "rating": review.rating,
                    "comment": review.comment
                    }
                    )
    
    return ratings

@router.get("/{user_id}/shoes")
def get_user_collection(user_id: int):
    """ """
    with db.engine.begin() as connection:
        collection = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT shoes.shoe_id, name, brand, color, material, price FROM shoes
                                                    JOIN shoes_to_users AS join_table ON join_table.shoe_id = shoes.shoe_id
                                                    WHERE join_table.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
        
    shoes = []

    for shoe in collection:
        shoes.append(
                {
                "shoe_id": shoe.shoe_id,
                "shoe_name": shoe.name,
                "brand": shoe.brand,
                "color": shoe.color,
                "material": shoe.material,
                "price": shoe.price
                }
        )
    return shoes

@router.get("/search/", tags=["search"])
def search_users(
    search_value: str = "",
    search_page: str = ""
):
    
    limit = 30
    
    if search_page == "":
        search_page = 0
    else:
        search_page = int(search_page)

    stmt = (
        sqlalchemy.select(
            db.users.c.username,
            db.users.c.name

        )
        .offset(search_page)
        .limit(limit)
    )


    counting = (
        sqlalchemy.select(
            sqlalchemy.func.count().label("count")
        )
        .select_from(db.users)
    )

    stmt = stmt.where(or_(db.users.c.username.ilike(f"%{search_value}%"),db.users.c.name.ilike(f"%{search_value}%")))
    counting = counting.where(or_(db.users.c.username.ilike(f"%{search_value}%"),db.users.c.name.ilike(f"%{search_value}%")))

    with db.engine.connect() as conn:

        result = conn.execute(stmt)
        count = conn.execute(counting).scalar_one()

        json = []
        for row in result:
            json.append(
                {
                    "name":row.name,
                    "username": row.username
                }
            )

    
    #calculate search page here
    prev = ""
    next = ""

    if search_page-limit >= 0:
        prev = str(search_page-limit)

    if search_page+limit < count:
        next = str(search_page+limit)

    return {
        "previous": prev,
        "next": next, 
        "results": json
    }

@router.get("/{user_id}/orders")
def get_orders(user_id: int):
    """ """
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


        orders = connection.execute(sqlalchemy.text(
                                                    """
                                                    SELECT orders.created_at,shoes.shoe_id,brand,name,quantity FROM orders
                                                    JOIN shoes ON shoes.shoe_id = orders.shoe_id
                                                    WHERE orders.user_id = :user_id
                                                    """),
                                                    [{"user_id": user_id}])
        
    ret = []

    for order in orders:
        ret.append(
                {
                "shoe_id": order.shoe_id,
                "brand": order.brand,
                "shoe_name": order.name,
                "quantity": order.quantity,
                "order_time": order.created_at.ctime(),
                }
        )
    return ret

@router.get("/{user_id}/points")
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