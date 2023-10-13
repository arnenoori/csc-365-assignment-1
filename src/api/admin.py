from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """
    with db.engine.begin() as connection:
        # Reset gold in global_inventory
        sql_query = """
        UPDATE global_inventory
        SET gold = 100
        """
        connection.execute(sqlalchemy.text(sql_query))
        # Reset quantity in potions
        sql_query = """
        UPDATE potions
        SET quantity = 0
        """
        connection.execute(sqlalchemy.text(sql_query))

    return "OK"

@router.get("/shop_info/")
def get_shop_info():
    """ """
    with db.engine.begin() as connection:
        # Fetch gold from global_inventory
        sql_query = """SELECT gold from global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        gold = result.first()[0]
        # Fetch quantity of each potion
        sql_query = """SELECT name, quantity FROM potions"""
        result = connection.execute(sqlalchemy.text(sql_query))
        potions = [dict(row) for row in result.fetchall()]

    return {
        "shop_name": "Potion Shop",
        "shop_owner": "Potion Seller",
        "inventory": {
            "gold": gold,
            "potions": potions
        }
    }