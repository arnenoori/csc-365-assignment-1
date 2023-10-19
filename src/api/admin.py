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
    inventory, all barrels are removed from inventory, and all in-flight carts are deleted. 
    """
    with db.engine.begin() as connection:
        # Reset global inventory
        sql_query = """
        UPDATE global_inventory
        SET num_red_ml = 0, num_green_ml = 0, num_blue_ml = 0, num_dark_ml = 0, gold = 100
        """
        connection.execute(sqlalchemy.text(sql_query))

        # Reset catalog quantity
        sql_query = """
        UPDATE catalog
        SET quantity = 0
        """
        connection.execute(sqlalchemy.text(sql_query))

        # Delete all items in carts
        sql_query = """
        DELETE FROM cart_items
        """
        connection.execute(sqlalchemy.text(sql_query))

        # Delete all in-flight carts
        sql_query = """
        DELETE FROM carts
        """
        connection.execute(sqlalchemy.text(sql_query))

    return "OK"

@router.get("/shop_info/")
def get_shop_info():
    """ """
    with db.engine.begin() as connection:
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml, gold from global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        first_row = result.first()

    if first_row is None:
        return {
            "shop_name": "The Enchanted Elixir Emporium",
            "shop_owner": "Potion Seller",
            "inventory": {
                "ml_in_red_barrels": 0,
                "ml_in_green_barrels": 0,
                "ml_in_blue_barrels": 0,
                "ml_in_dark_barrels": 0,
                "gold": 100
            }
        }

    return {
        "shop_name": "The Enchanted Elixir Emporium",
        "shop_owner": "Potion Seller",
        "inventory": {
            "ml_in_red_barrels": first_row.num_red_ml,
            "ml_in_green_barrels": first_row.num_green_ml,
            "ml_in_blue_barrels": first_row.num_blue_ml,
            "ml_in_dark_barrels": first_row.num_dark_ml,
            "gold": first_row.gold
        }
    }