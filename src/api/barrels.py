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
def post_deliverundefinedbarrels(barrels_delivered: list[Barrel]):
    for barrel in barrels_delivered:
        with db.engine.begin() as connection:
            total_ml = barrel.ml_per_barrel * barrel.quantity

            # Update the global inventory for each potion type
            for i, potion_percentage in enumerate(barrel.potion_type):
                if potion_percentage > 0:
                    potion_ml = total_ml * (potion_percentage / 100)
                    # Update the global inventory 
                    sql_query = f"""
                    UPDATE global_inventory
                    SET ml = ml + {potion_ml}, quantity = quantity + {barrel.quantity}
                    WHERE potion_id = {i}
                    """
                    connection.execute(sqlalchemy.text(sql_query))

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    purchase_plan = []
    with db.engine.begin() as connection:
        for barrel in wholesale_catalog:
            sql_query = f"""SELECT gold FROM global_inventory"""
            result = connection.execute(sqlalchemy.text(sql_query))
            gold = result.first().gold

            if gold >= barrel.price:
                purchase_plan.append({
                    "sku": barrel.sku,
                    "quantity": 1,
                })
                sql_query = f"""
                UPDATE global_inventory
                SET gold = gold - {barrel.price}
                """
                connection.execute(sqlalchemy.text(sql_query))

    return purchase_plan