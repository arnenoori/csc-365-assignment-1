from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str
    ml_per_barrel: int
    potion_type: list[int]
    price: int
    quantity: int

@router.post("/deliver")
# Works
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    for barrel in barrels_delivered:
        # Ensure potion_type has 4 elements
        while len(barrel.potion_type) < 4:
            barrel.potion_type.append(0)

        with db.engine.begin() as connection:
            sql_query = f"""
            UPDATE global_inventory
            SET num_red_ml = num_red_ml + {barrel.potion_type[0] * barrel.ml_per_barrel * barrel.quantity},
                num_green_ml = num_green_ml + {barrel.potion_type[1] * barrel.ml_per_barrel * barrel.quantity},
                num_blue_ml = num_blue_ml + {barrel.potion_type[2] * barrel.ml_per_barrel * barrel.quantity},
                num_dark_ml = num_dark_ml + {barrel.potion_type[3] * barrel.ml_per_barrel * barrel.quantity}
            """
            connection.execute(sqlalchemy.text(sql_query))

    return "OK"


# Gets called once a day
@router.post("/plan")
# Works
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    purchase_plan = []
    with db.engine.begin() as connection:
        for barrel in wholesale_catalog:
            sql_query = f"""SELECT gold, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
            result = connection.execute(sqlalchemy.text(sql_query))
            inventory = result.first()

            if inventory is None:
                return {
                    "gold": 0,
                    "num_red_ml": 0,
                    "num_green_ml": 0,
                    "num_blue_ml": 0,
                    "num_dark_ml": 0
                }

            gold, red_ml, green_ml, blue_ml, dark_ml = inventory

            if gold >= barrel.price:
                purchase_plan.append({
                    "sku": barrel.sku,
                    "quantity": 1,
                })
                sql_query = f"""
                UPDATE global_inventory
                SET gold = gold - {barrel.price},
                    num_red_ml = num_red_ml - {barrel.potion_type[0] * barrel.ml_per_barrel},
                    num_green_ml = num_green_ml - {barrel.potion_type[1] * barrel.ml_per_barrel},
                    num_blue_ml = num_blue_ml - {barrel.potion_type[2] * barrel.ml_per_barrel},
                    num_dark_ml = num_dark_ml - {barrel.potion_type[3] * barrel.ml_per_barrel}
                """
                connection.execute(sqlalchemy.text(sql_query))

    return purchase_plan

""""

[Barrel(sku='SMALL_RED_BARREL', ml_per_barrel=500, potion_type=[1, 0, 0, 0], price=100, quantity=1) 
Barrel(sku='MINI_RED_BARREL', ml_per_barrel=200, potion_type=[1, 0, 0, 0], price=60, quantity=1)

Barrel(sku='SMALL_BLUE_BARREL', ml_per_barrel=500, potion_type=[0, 0, 1, 0], price=120, quantity=1)
Barrel(sku='MINI_BLUE_BARREL', ml_per_barrel=200, potion_type=[0, 0, 1, 0], price=60, quantity=1)]

Barrel(sku='SMALL_GREEN_BARREL', ml_per_barrel=500, potion_type=[0, 1, 0, 0], price=100, quantity=1) 
Barrel(sku='MINI_GREEN_BARREL', ml_per_barrel=200, potion_type=[0, 1, 0, 0], price=60, quantity=1) 
    
"""