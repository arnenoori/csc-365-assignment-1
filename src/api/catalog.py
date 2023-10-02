from fastapi import APIRouter
from src import database as db
import sqlalchemy

router = APIRouter()

@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    # Can return a max of 20 items.

    # Fetch the number of red potions from the database
    with db.engine.begin() as connection:
        sql_query = """SELECT num_red_potions FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        num_red_potions = result.first().num_red_potions

    # Return the catalog with the quantity of red potions
    return [
            {
                "sku": "RED_POTION_0",
                "name": "red potion",
                "quantity": num_red_potions,
                "price": 50,
                "potion_type": [100, 0, 0, 0],
            }
        ]