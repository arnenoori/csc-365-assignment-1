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
        sql_query = """
        UPDATE global_inventory
        SET num_red_potions = 0, num_red_ml = 0, gold = 100
        """
        connection.execute(sqlalchemy.text(sql_query))

    return "OK"

@router.get("/shop_info/")
def get_shop_info():
    """ """
    with db.engine.begin() as connection:
        sql_query = """SELECT num_red_potions, num_red_ml, gold from global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        first_row = result.first()

    return {
        "shop_name": "Potion Shop",
        "shop_owner": "Potion Seller",
        "inventory": {
            "number_of_red_potions": first_row.num_red_potions,
            "ml_in_red_barrels": first_row.num_red_ml,
            "gold": first_row.gold
        }
    }