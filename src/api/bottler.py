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
    potion_type: int
    quantity: int

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):
    """ """
    for potion in potions_delivered:
        # Insert a new transaction and ledger entry
        with db.engine.begin() as connection:
            sql_query = f"""
            INSERT INTO inventory_transactions (description)
            VALUES ('Delivered {potion.quantity} of potion type {potion.potion_type}');

            INSERT INTO inventory_ledger_entries (inventory_id, transaction_id, change)
            VALUES ({potion.potion_type}, (SELECT id FROM inventory_transactions ORDER BY id DESC LIMIT 1), {potion.quantity});
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

    # Initial logic: bottle all barrels into red, blue, and green potions.
    with db.engine.begin() as connection:
        sql_query = """
        SELECT p.potion_type, SUM(ile.change) AS quantity
        FROM inventory_ledger_entries ile
        JOIN potions p ON ile.inventory_id = p.id
        GROUP BY p.potion_type;
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        potions = result.fetchall()

        bottle_plan = []
        for potion in potions:
            potion_type, quantity = potion
            if sum(potion_type) == 100 and quantity > 0:
                bottle_plan.append({
                    "potion_type": potion_type,
                    "quantity": quantity,
                })

    return bottle_plan


