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
        # Fetch the gold_id first
        gold_id_query = "SELECT id FROM global_inventory WHERE name = 'gold';"
        gold_id_result = connection.execute(sqlalchemy.text(gold_id_query))
        gold_id = gold_id_result.first().id
        print(f"Gold ID: {gold_id}") 

        for barrel in wholesale_catalog:
            sql_query = """
            SELECT SUM(change) AS gold
            FROM inventory_ledger_entries
            WHERE inventory_id = :gold_id;
            """
            result = connection.execute(sqlalchemy.text(sql_query), {"gold_id": gold_id})
            gold = result.first().gold
            print(f"Gold: {gold}") 
            if gold >= barrel.price:
                print(f"Purchasing Barrel: {barrel.sku}")  # trying to see if I'm buying anything
                purchase_plan.append({
                    "sku": barrel.sku,
                    "quantity": 1,
                })
                sql_query = f"""
                INSERT INTO inventory_transactions (description)
                VALUES ('Purchased {barrel.sku} for {barrel.price} gold');

                INSERT INTO inventory_ledger_entries (inventory_id, transaction_id, change)
                VALUES (:gold_id, (SELECT id FROM inventory_transactions ORDER BY id DESC LIMIT 1), -{barrel.price});
                """
                connection.execute(sqlalchemy.text(sql_query), {"gold_id": gold_id})

    return purchase_plan