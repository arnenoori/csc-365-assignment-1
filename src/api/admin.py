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
        # Query global_inventory
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml, gold FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        global_inventory = result.first()

        if global_inventory is None:
            print("No inventory found.")
            return "No inventory found."

        num_red_ml, num_green_ml, num_blue_ml, num_dark_ml, gold = global_inventory

        # Create a new transaction
        sql_query = """
        INSERT INTO inventory_transactions (description)
        VALUES (:description)
        RETURNING id
        """
        transaction_id = connection.execute(sqlalchemy.text(sql_query), {"description": "Reset game state"}).scalar()

        # Create ledger entries for each change in inventory
        sql_query = """
        INSERT INTO inventory_ledger_entries (inventory_type, transaction_id, change)
        VALUES (:inventory_type, :transaction_id, :change)
        """
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "gold", "transaction_id": transaction_id, "change": 100 - gold})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "red_ml", "transaction_id": transaction_id, "change": -num_red_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "green_ml", "transaction_id": transaction_id, "change": -num_green_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "blue_ml", "transaction_id": transaction_id, "change": -num_blue_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "dark_ml", "transaction_id": transaction_id, "change": -num_dark_ml})
        
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