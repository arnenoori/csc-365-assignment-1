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
    # Fetch all potions from the database
    with db.engine.begin() as connection:
        sql_query = """SELECT name, potion_type, price, quantity FROM potions"""
        result = connection.execute(sqlalchemy.text(sql_query))
        potions = result.fetchall()
        catalog = []
        for potion in potions:
            # Limit the quantity to a maximum of 20
            quantity = max(0, min(potion[3], 20))

            if quantity > 0:
                catalog.append({
                    "sku": f"{potion[0].upper()}_POTION_{potion[1]}",
                    "name": potion[0],
                    "quantity": quantity,
                    "price": potion[2],
                    "potion_type": potion[1],
                })

    return catalog