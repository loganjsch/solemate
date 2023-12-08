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
    prefix="/brands",
    tags=["brands"],
    dependencies=[Depends(auth.get_api_key)],
)

class Shoe(BaseModel):
    name: str
    brand: str
    price: int
    color: str
    material: str
    tags: list[str]
    type: str

@router.post("/{brand_id}/shoes")
def post_shoe(brand_id:int, new_shoe: Shoe):
    """Add new shoe to the app"""
    

    with db.engine.begin() as connection:
        #Authentication
        response = connection.execute(sqlalchemy.text("""
                                                SELECT is_logged_in
                                                FROM brands
                                                WHERE brand_id = :brand_id
                                            """),
                                            [{"brand_id": brand_id}]).scalar_one()
            
        if response != True:
                return "Login to Access this feature"
        #####
    

        connection.execute(sqlalchemy.text("""
            INSERT INTO shoes (name, brand, price, color, material, tags, type)
            VALUES (:name, :brand, :price, :color, :material, :tags, :type)
        """), {"name": new_shoe.name, "brand": new_shoe.brand, "price": new_shoe.price, "color": new_shoe.color, "material": new_shoe.material, "tags": new_shoe.tags, "type": new_shoe.type})

        return "OK"

@router.post("/")
def create_brand(brand_name: str, email: str, password: str):
    """ """

    #check if password long enough
    if len(password) < 8:
        return "Password must be atleast 8 characters"

    #check for valid email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(not re.fullmatch(regex, email)):
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

    password = f.encrypt(bytes(password,'utf-8'))


    with db.engine.begin() as connection:
        #check if brand name already in use
        validBrand = connection.execute(sqlalchemy.text("""
                                                SELECT brand_name FROM brands
                                                WHERE brand_name = :brand_name
                                            """),
                                            [{"brand_name": brand_name}]).all()
        
        if len(validBrand) > 0:
            return "Brand Name Already In Use"
        
        #check if email already in use
        validEmail = connection.execute(sqlalchemy.text("""
                                                SELECT email FROM brands
                                                WHERE email = :email
                                            """),
                                            [{"email": email}]).all()
        
        if len(validEmail) > 0:
            return "Email Already In Use. Use Another Email"

        try:
            connection.execute(sqlalchemy.text("""
                                            INSERT INTO brands (brand_name, email, password,salt) 
                                            VALUES (:brand_name, :email, :password,:salt)
                                            """),
                                            [{"brand_name": brand_name, "email": email, "password": password,"salt":salt}])
        except Exception as error:
             print("Couldn't Create Account")
        

    return "Account Successfully Created. Please Login to Continue"

@router.post("/login")
def login(brand_name: str, password: str):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
                                            SELECT password,salt
                                            FROM brands
                                            WHERE brand_name = :brand_name
                                           """),
                                        [{"brand_name": brand_name}]).first()
    
        if not response:
            return "Invalid Brand Name"
        
        #Get key for decryption
        dotenv.load_dotenv()
        crypto_key = bytes(os.environ.get("CRYPTO_KEY"),'utf-8')
        
        #get brand values from database
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
                                            UPDATE brands
                                            SET is_logged_in = TRUE
                                            WHERE brand_name = :brand_name
                                           """),
                                        [{"brand_name": brand_name}])

            return "Logged In"
        else:
            return "Incorrect Password"
        
@router.post("/{brand_id}/logout")
def logout(brand_id:int):
    with db.engine.begin() as connection:
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM brands
                                            WHERE brand_id = :brand_id
                                           """),
                                        [{"brand_id": brand_id}]).scalar_one()
        
        if response != True:
            return "Cannot Logout"
        
        connection.execute(sqlalchemy.text("""
                                            UPDATE brands
                                            SET is_logged_in = FALSE
                                            WHERE brand_id = :brand_id
                                           """),
                                        [{"brand_id": brand_id}])

        return "Logged Out"