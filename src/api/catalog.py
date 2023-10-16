from fastapi import APIRouter
from src import database as db
import sqlalchemy

router = APIRouter()

@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    # Fetch the catalog from the database
    with db.engine.begin() as connection:
        sql_query = """SELECT sku, name, quantity, price, array[num_red_ml, num_green_ml, num_blue_ml, num_dark_ml] as potion_type FROM catalog"""
        result = connection.execute(sqlalchemy.text(sql_query))
        catalog = result.fetchall()

    # Convert the catalog to the required format
    catalog = [{
        "sku": row[0],
        "name": row[1],
        "quantity": row[2],
        "price": row[3],
        "potion_type": row[4],
    } for row in catalog]

    return catalog