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

    # Generate the catalog dynamically based on the potions in the database
    catalog = []
    for potion in potions:
        # Limit the quantity to a maximum of 20
        quantity = max(0, min(potion['quantity'], 20))

        if quantity > 0:
            catalog.append({
                "sku": f"{potion['name'].upper()}_POTION_0",
                "name": potion['name'],
                "quantity": quantity,
                "price": potion['price'],
                "potion_type": potion['potion_type'],
            })

    return catalog   