from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/shoes",
    tags=["shoes"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    user_id: int
    name: str
    username: str
    email: str
    password: str

class Shoe(BaseModel):
    shoe_id: int
    name: str
    brand: str
    price: int
    color: str
    material: str
    tags: list[str]
    type: str

class Rating(BaseModel):
    shoe_id: int
    user_id: int
    rating: int
    comment: str

@router.get("/{shoe_id}")
def get_shoe(shoe_id: int):
    """ """
    if shoe_id < 0:
        raise HTTPException(status_code=400, detail="Invalid id")

    with db.engine.begin() as connection:
        shoe = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT shoes.shoe_id,name,brand,price,color,material,tags,type, AVG(rating) as avg
                                                FROM shoes
                                                LEFT JOIN reviews ON reviews.shoe_id = shoes.shoe_id
                                                WHERE shoes.shoe_id = :shoe_id
                                                GROUP BY shoes.shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}]).first()

    # Check if the shoe with the specified ID exists
    if shoe is None:
        raise HTTPException(status_code=404, detail="Shoe not found")

    return {
        "shoe_id": shoe.shoe_id,
        "name": shoe.name,
        "brand": shoe.brand,
        "price": shoe.price,
        "color": shoe.color,
        "material": shoe.material,
        "tags": shoe.tags,
        "type": shoe.type,
        "rating": round(shoe.avg,2)
        }

@router.get("/{shoe_id}/reviews")
def get_shoe_reviews(shoe_id: int):
    """ """
    with db.engine.begin() as connection:
    # Check if the shoe exists
        shoe_exists = connection.execute(sqlalchemy.text(
            """
            SELECT COUNT(*) 
            FROM shoes 
            WHERE shoe_id = :shoe_id
            """), {"shoe_id": shoe_id}).scalar_one()

        if shoe_exists == 0:
            raise HTTPException(status_code=404, detail=f"Shoe not found")

        reviews = []

        review_list = connection.execute(sqlalchemy.text(
                                                """
                                                SELECT * 
                                                FROM reviews
                                                WHERE shoe_id = :shoe_id
                                                """), 
                                                [{"shoe_id": shoe_id}])
    
    for review in review_list:
        reviews.append(
                    {
                    "user_id": review.user_id,
                    "rating": review.rating,
                    "comment": review.comment
                    }
                    )
    if not reviews:
            return {"message": "No reviews found for this shoe"}
    return reviews

@router.post("/{shoe_id}/reviews/{user_id}")
def post_shoe_review(review:Rating):
    """ """
    
    with db.engine.begin() as connection:
        ### Authentication
        response = connection.execute(sqlalchemy.text("""
                                            SELECT is_logged_in
                                            FROM users
                                            WHERE user_id = :user_id
                                           """),
                                        [{"user_id": review.user_id}]).scalar_one()
        
        if not response:
            raise HTTPException(status_code=401, detail="Login to post review")
        #####
        #check if user added shoe to profile
        user_shoe = connection.execute(sqlalchemy.text("""
            SELECT * FROM shoes_to_users
            WHERE user_id = :user_id AND shoe_id = :shoe_id
        """), {"user_id": review.user_id, "shoe_id": review.shoe_id}).fetchone()

        if not user_shoe:
           raise HTTPException(status_code=400, detail="User has not added this shoe to their profile")
        
        #check for valid rating
        if review.rating > 5 or review.rating < 1:
            return "INVALID RATING (1-5 INCLUSIVE)"
        
        #check for valid comment
        if len(review.comment) > 500:
            return "Comment Cannoct Exceed 500 Characters"

        # Check if the user has already reviewed this shoe
        existing_review = connection.execute(sqlalchemy.text("""
            SELECT * FROM reviews
            WHERE user_id = :user_id AND shoe_id = :shoe_id
        """), {"user_id": review.user_id, "shoe_id": review.shoe_id}).fetchone()

        if existing_review:
            raise HTTPException(status_code=400, detail="User has already reviewed this shoe")
        
        #check how many points were earned in last 24 hours
        points24 = connection.execute(sqlalchemy.text("""
                                           SELECT COALESCE(SUM(point_change),0)
                                           FROM point_ledger
                                           WHERE user_id = :user_id AND created_at >= NOW() - '1 day'::INTERVAL AND point_change > 0
                                            
                                           """),
                                        [{"user_id": review.user_id}]).scalar_one()
        
        #insert points so total for last 24 hours <= 100
        point_change = min(100-points24,len(review.comment)//10)
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO point_ledger (user_id,point_change) 
                                           VALUES (:user_id,:point_change)
                                           """),
                                        [{"user_id": review.user_id,"point_change":point_change}])
        
        #insert review into reviews
        connection.execute(sqlalchemy.text("""
                                           INSERT INTO reviews (shoe_id, user_id, rating, comment) 
                                           VALUES (:shoe_id, :user_id, :rating, :comment)
                                           """),
                                        [{"shoe_id": review.shoe_id, "user_id": review.user_id, "rating": review.rating, "comment": review.comment}])

    return "Points Earned: " + str(point_change)

@router.delete("/reviews/delete/{rating_id}")
def delete_shoe_review(rating_id: int):
    with db.engine.begin() as connection:
        review = connection.execute(sqlalchemy.text("""
            SELECT user_id, comment FROM reviews
            WHERE rating_id = :rating_id
        """), {"rating_id": rating_id}).fetchone()

        if not review:
            return "Review not found"

        points_to_deduct = len(review.comment) // 10

        connection.execute(sqlalchemy.text("""
            INSERT INTO point_ledger (user_id, point_change)
            VALUES (:user_id, :point_change)
        """), {"user_id": review.user_id, "point_change": -points_to_deduct})

        connection.execute(sqlalchemy.text("""
            DELETE FROM reviews
            WHERE rating_id = :rating_id
        """), {"rating_id": rating_id})

        return "Review and points deleted successfully"

@router.get("/compare/{shoe_id_1}/{shoe_id_2}")
def compare_shoes(shoe_id_1: int, shoe_id_2: int):
    """"""
    #TODO Edge case 1 (Rohit) - Add exceptions for non existent shoe_id
    with db.engine.begin() as connection:
        shoe1 = connection.execute(sqlalchemy.text("""
            SELECT s.shoe_id, s.name, s.brand, s.price, AVG(r.rating) as avg_rating
            FROM shoes s
            LEFT JOIN reviews r ON r.shoe_id = s.shoe_id
            WHERE s.shoe_id = :shoe_id_1
            GROUP BY s.shoe_id, s.name, s.brand, s.price
        """), {"shoe_id_1": shoe_id_1}).fetchone()

        shoe2 = connection.execute(sqlalchemy.text("""
            SELECT s.shoe_id, s.name, s.brand, s.price, AVG(r.rating) as avg_rating
            FROM shoes s
            LEFT JOIN reviews r ON r.shoe_id = s.shoe_id
            WHERE s.shoe_id = :shoe_id_2
            GROUP BY s.shoe_id, s.name, s.brand, s.price
        """), {"shoe_id_2": shoe_id_2}).fetchone()

        # Check if either shoe_id does not exist
        if shoe1 is None:
            raise HTTPException(status_code=404, detail=f"Shoe with ID {shoe_id_1} not found")
        
        if shoe2 is None:
            raise HTTPException(status_code=404, detail=f"Shoe with ID {shoe_id_2} not found")

         # Extract average ratings and handle None values
        avg_rating_1 = round(shoe1.avg_rating, 2) if shoe1.avg_rating is not None else "N/A"
        avg_rating_2 = round(shoe2.avg_rating, 2) if shoe2.avg_rating is not None else "N/A"

        response = {
            "shoe_ids":[shoe1.shoe_id, shoe2.shoe_id],
            "shoe_names": [shoe1.name, shoe2.name],
            "brands":[shoe1.brand, shoe2.brand],
            "retail_prices":[shoe1.price, shoe2.price],
            "ratings":[avg_rating_1, avg_rating_2]
        }

        return response
