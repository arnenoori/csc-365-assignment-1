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
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    for barrel in barrels_delivered:
        total_ml = barrel.ml_per_barrel * barrel.quantity
        # Update the global inventory for each potion type
        for i, potion_percentage in enumerate(barrel.potion_type):
            if potion_percentage > 0:
                potion_ml = total_ml * (potion_percentage / 100)
                # Insert a new transaction and ledger entry
                with db.engine.begin() as connection:
                    sql_query = f"""
                    INSERT INTO inventory_transactions (description)
                    VALUES ('Delivered {barrel.quantity} barrels of potion {i}');

                    INSERT INTO inventory_ledger_entries (inventory_id, transaction_id, change)
                    VALUES ({i}, (SELECT id FROM inventory_transactions ORDER BY id DESC LIMIT 1), {potion_ml});
                    """
                    connection.execute(sqlalchemy.text(sql_query))

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    print(f"Wholesale Catalog: {wholesale_catalog}") 
    purchase_plan = []
    with db.engine.begin() as connection:
        # Fetch the gold first
        gold_query = "SELECT gold FROM global_inventory WHERE id = 1;"
        gold_result = connection.execute(sqlalchemy.text(gold_query))
        gold = gold_result.first().gold
        print(f"Gold: {gold}") 

        # Fetch the current inventory
        inventory_query = "SELECT * FROM inventory;"
        inventory_result = connection.execute(sqlalchemy.text(inventory_query))
        inventory = inventory_result.fetchall()

        for barrel in wholesale_catalog:
            # Check if we need this potion type
            if inventory[barrel.potion_type.index(1)] < 10 and gold >= barrel.price:
                print(f"Purchasing Barrel: {barrel.sku}")  # trying to see if I'm buying anything
                purchase_plan.append({
                    "sku": barrel.sku,
                    "quantity": 1,
                })
                gold -= barrel.price  # Update the gold amount

    return purchase_plan