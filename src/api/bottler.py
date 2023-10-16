from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):
    for potion in potions_delivered:
        with db.engine.begin() as connection:
            sql_query = f"""
            UPDATE global_inventory
            SET num_red_potions = num_red_potions + {potion.potion_type[0] * potion.quantity},
                num_green_potions = num_green_potions + {potion.potion_type[1] * potion.quantity},
                num_blue_potions = num_blue_potions + {potion.potion_type[2] * potion.quantity},
                num_dark_potions = num_dark_potions + {potion.potion_type[3] * potion.quantity}
            """
            connection.execute(sqlalchemy.text(sql_query))

    return "OK"

@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """
    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.
    bottle_plan = []

    with db.engine.begin() as connection:
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        num_red_ml, num_green_ml, num_blue_ml, num_dark_ml = result.first()

        # Create a bottle plan based on the current inventory
        for potion_type in [[100, 0, 0, 0], [0, 100, 0, 0], [0, 0, 100, 0], [0, 0, 0, 100]]:
            quantity = min(num_red_ml // potion_type[0] if potion_type[0] != 0 else float('inf'),
                           num_green_ml // potion_type[1] if potion_type[1] != 0 else float('inf'),
                           num_blue_ml // potion_type[2] if potion_type[2] != 0 else float('inf'),
                           num_dark_ml // potion_type[3] if potion_type[3] != 0 else float('inf'))

            if quantity > 0:
                bottle_plan.append({
                    "potion_type": potion_type,
                    "quantity": quantity,
                })

                # Update the inventory
                num_red_ml -= potion_type[0] * quantity
                num_green_ml -= potion_type[1] * quantity
                num_blue_ml -= potion_type[2] * quantity
                num_dark_ml -= potion_type[3] * quantity

    return bottle_plan