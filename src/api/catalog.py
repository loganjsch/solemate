from fastapi import APIRouter, Depends
from src.api import auth
import sqlalchemy
from src import database as db
from sqlalchemy import func,or_


router = APIRouter(
    dependencies=[Depends(auth.get_api_key)]
)


@router.get("/shoes", tags=["shoes"])
def get_shoe_catalog():
    """ """
    with db.engine.begin() as connection:
        catalog = connection.execute(sqlalchemy.text("""SELECT shoes.shoe_id,name,brand,AVG(rating) as avg
                                                     FROM shoes 
                                                     LEFT JOIN reviews ON shoes.shoe_id = reviews.shoe_id
                                                     GROUP BY shoes.shoe_id
                                                     ORDER BY RANDOM()
                                                     LIMIT 10"""))
    ret = []
    for shoe in catalog:
        ret.append(
            {
                "name": shoe.name,
                "brand": shoe.brand,
                "avg_rating": shoe.avg
            }
        )
    return ret



@router.get("/shoes/search", tags=["search"])
def search_shoes(
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
            db.shoes.c.shoe_id,
            db.shoes.c.name,
            db.shoes.c.brand,
            db.shoes.c.price,
            func.avg(db.reviews.c.rating).label("avg")
        )
        .join(db.reviews,db.reviews.c.shoe_id == db.shoes.c.shoe_id,isouter=True)
        .group_by(db.shoes.c.shoe_id)
        .offset(search_page)
        .limit(limit)
        .order_by(db.shoes.c.shoe_id)
    )


    counting = (
        sqlalchemy.select(
            sqlalchemy.func.count().label("count")
        )
        .select_from(db.shoes)
    )

    stmt = stmt.where(or_(db.shoes.c.name.ilike(f"%{search_value}%"),
                          db.shoes.c.brand.ilike(f"%{search_value}%"),
                          db.shoes.c.type.ilike(f"%{search_value}%"),
                          db.shoes.c.color.ilike(f"%{search_value}%"),
                          db.shoes.c.material.ilike(f"%{search_value}%"),
                          func.array_to_string(db.shoes.c.tags,',').ilike(f"%{search_value}%")))
    
    counting = counting.where(or_(db.shoes.c.name.ilike(f"%{search_value}%"),
                          db.shoes.c.brand.ilike(f"%{search_value}%"),
                          db.shoes.c.type.ilike(f"%{search_value}%"),
                          db.shoes.c.color.ilike(f"%{search_value}%"),
                          db.shoes.c.material.ilike(f"%{search_value}%"),
                          func.array_to_string(db.shoes.c.tags,',').ilike(f"%{search_value}%")))

    with db.engine.connect() as conn:

        result = conn.execute(stmt)
        count = conn.execute(counting).scalar_one()

        json = []
        for row in result:
            json.append(
                {
                    "shoe_id": row.shoe_id,
                    "shoe_name": row.name,
                    "brand": row.brand,
                    "price": row.price,
                    "rating": row.avg,
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