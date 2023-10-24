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
    print("Starting delivery of barrels...")
    for barrel in barrels_delivered:
        # Ensure potion_type has 4 elements
        while len(barrel.potion_type) < 4:
            barrel.potion_type.append(0)

        # Log the barrel data
        print(f"Barrel data: {barrel}")

        with db.engine.begin() as connection:
            # Create a new transaction
            sql_query = """
            INSERT INTO inventory_transactions (description)
            VALUES (:description)
            RETURNING id
            """
            transaction_id = connection.execute(sqlalchemy.text(sql_query), {"description": "Barrel delivery"}).scalar()

            # Create ledger entries for each change in inventory
            sql_query = """
            INSERT INTO inventory_ledger_entries (inventory_type, transaction_id, change)
            VALUES (:inventory_type, :transaction_id, :change)
            """
            connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "gold", "transaction_id": transaction_id, "change": -barrel.price})
            connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_red_ml", "transaction_id": transaction_id, "change": barrel.ml_per_barrel * barrel.potion_type[0]})
            connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_green_ml", "transaction_id": transaction_id, "change": barrel.ml_per_barrel * barrel.potion_type[1]})
            connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_blue_ml", "transaction_id": transaction_id, "change": barrel.ml_per_barrel * barrel.potion_type[2]})
            connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_dark_ml", "transaction_id": transaction_id, "change": barrel.ml_per_barrel * barrel.potion_type[3]})

        print(f"Delivered barrel: {barrel.sku}")
        
    print("Finished delivery of barrels.")
    return "OK"


# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    print("Starting wholesale purchase plan...")
    with db.engine.begin() as connection:
        # Calculate the current inventory values
        sql_query = """
            SELECT 
                (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'gold') AS gold,
                (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'red_ml') AS red_ml,
                (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'green_ml') AS green_ml,
                (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'blue_ml') AS blue_ml,
                (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'dark_ml') AS dark_ml
        """
        inventory = connection.execute(sqlalchemy.text(sql_query)).first()

    if inventory is None:
        gold, red_ml, green_ml, blue_ml, dark_ml = 0, 0, 0, 0, 0
    else:
        gold, red_ml, green_ml, blue_ml, dark_ml = inventory

    purchase_plan = []

    def buy_potion(potion_type, ml_needed):
        nonlocal gold
        for barrel in wholesale_catalog:
            if barrel.potion_type == potion_type and barrel.price <= gold:
                gold -= barrel.price  # buying only one barrel for now
                purchase_plan.append({"sku": barrel.sku, "quantity": 1})  # quantity is set to 1
                print(f"Bought barrel: {barrel.sku}")
                return barrel.ml_per_barrel  # assuming one barrel is bought, so not multiplying by quantity
        return 0

    if red_ml < 500 and gold > 0:
        red_ml += buy_potion([1, 0, 0, 0], 500 - red_ml)
    if green_ml < 500 and gold > 0:
        green_ml += buy_potion([0, 1, 0, 0], 500 - green_ml)
    if blue_ml < 500 and gold > 0:
        blue_ml += buy_potion([0, 0, 1, 0], 500 - blue_ml)

    # handles the case where any potion is less than 100ml
    # and buys the smallest available barrel that the remaining gold can afford.
    potions = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]  # red, green, blue
    ml_values = [red_ml, green_ml, blue_ml]  # current ml values of potions

    for i, potion in enumerate(potions):
        if ml_values[i] < 100 and gold > 0:
            for barrel in sorted(wholesale_catalog, key=lambda x: x.ml_per_barrel):  # smallest barrel first
                if barrel.potion_type == potion and gold >= barrel.price:
                    purchase_plan.append({"sku": barrel.sku, "quantity": 1})
                    gold -= barrel.price
                    print(f"Bought barrel: {barrel.sku}")
                    break  # break after buying one barrel

    # Update the inventory after all purchases
    with db.engine.begin() as connection:
        # Create a new transaction
        sql_query = """
        INSERT INTO inventory_transactions (description)
        VALUES (:description)
        RETURNING id
        """
        transaction_id = connection.execute(sqlalchemy.text(sql_query), {"description": "Wholesale purchase plan"}).scalar()

        # Create ledger entries for each change in inventory
        sql_query = """
        INSERT INTO inventory_ledger_entries (inventory_type, transaction_id, change)
        VALUES (:inventory_type, :transaction_id, :change)
        """
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "gold", "transaction_id": transaction_id, "change": -gold})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_red_ml", "transaction_id": transaction_id, "change": red_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_green_ml", "transaction_id": transaction_id, "change": green_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_blue_ml", "transaction_id": transaction_id, "change": blue_ml})
        connection.execute(sqlalchemy.text(sql_query), {"inventory_type": "num_dark_ml", "transaction_id": transaction_id, "change": dark_ml})

    print("Finished wholesale purchase plan.")
    return purchase_plan  # returning the purchase plan instead of the inventory statuses

# barrel optimizer function