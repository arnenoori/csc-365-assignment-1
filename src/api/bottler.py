from fastapi import APIRouter, Depends
from enum import Enum
from typing import List
from pydantic import BaseModel
from src.api import auth
from src import database as db
from sqlalchemy import text
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: List[PotionInventory]):
    print("Starting delivery of potions...")
    with db.engine.begin() as connection:
        # Query global_inventory
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        global_inventory = result.first()

        if global_inventory is None:
            print("No inventory found.")
            return "No inventory found."

        num_red_ml, num_green_ml, num_blue_ml, num_dark_ml = global_inventory

        # Query catalog
        sql_query = """SELECT id, sku, name, price, quantity, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM catalog"""
        catalog = connection.execute(sqlalchemy.text(sql_query)).fetchall()

        MAX_QUANTITY = 10000

        for potion in potions_delivered:
            print(f"Processing potion: {potion}")
            if len(potion.potion_type) != 4:
                print(f"Error: potion.potion_type must contain exactly four elements, but got {len(potion.potion_type)}.")
                continue

            red_ml, green_ml, blue_ml, dark_ml = potion.potion_type
            sku = name = f"{red_ml}_{green_ml}_{blue_ml}_{dark_ml}"
            quantity = potion.quantity

            if quantity < 0:
                print(f"Error: Negative quantity ({quantity}) specified for potion: {potion}")
                continue

            updated_quantity = quantity

            if updated_quantity > MAX_QUANTITY:
                print(f"Error: Quantity ({updated_quantity}) exceeds the maximum limit for potion: {potion}")
                continue

            # Create a new transaction
            sql_query = """
            INSERT INTO inventory_transactions (description)
            VALUES (:description)
            RETURNING id
            """
            transaction_id = connection.execute(sqlalchemy.text(sql_query), {"description": f"Delivered potion: {potion}"}).scalar()

            # Create ledger entries for each change in inventory
            for i, change in enumerate(potion.potion_type):
                sql_query = """
                INSERT INTO inventory_ledger_entries (inventory_id, transaction_id, change)
                VALUES (:inventory_id, :transaction_id, :change)
                """
                connection.execute(sqlalchemy.text(sql_query), {"inventory_id": i+2, "transaction_id": transaction_id, "change": -change * quantity})

            print(f"Delivered potion: {potion}")

    print("Finished delivery of potions.")
    return "OK"

@router.post("/plan")
def get_bottle_plan():
    MAX_SAME_POTION = 10
    RESOURCE_THRESHOLD = 2000
    bottle_plan = []

    with db.engine.begin() as connection:
        # Calculate the current inventory values
        sql_query = """
        SELECT 
            (SELECT SUM(red_ml) FROM inventory_ledger_entries) AS red_ml,
            (SELECT SUM(green_ml) FROM inventory_ledger_entries) AS green_ml,
            (SELECT SUM(blue_ml) FROM inventory_ledger_entries) AS blue_ml,
            (SELECT SUM(dark_ml) FROM inventory_ledger_entries) AS dark_ml
        """
        inventory = connection.execute(sqlalchemy.text(sql_query)).first()

        if inventory is None:
            red_ml, green_ml, blue_ml, dark_ml = 0, 0, 0, 0
        else:
            red_ml, green_ml, blue_ml, dark_ml = inventory

        # Query catalog for potion recipes
        sql_query = """SELECT sku, name, quantity, price, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM catalog"""
        catalog = connection.execute(sqlalchemy.text(sql_query)).fetchall()

        for potion in catalog:
            sku, name, quantity, price, required_red, required_green, required_blue, required_dark = potion

            # Check if we have enough ingredients for at least one potion
            can_create = all([
                red_ml >= required_red if required_red > 0 else True,
                green_ml >= required_green if required_green > 0 else True,
                blue_ml >= required_blue if required_blue > 0 else True,
                dark_ml >= required_dark if required_dark > 0 else True
            ])

            if not can_create:
                print(f"Not enough inventory to create even one '{name}'. Skipping...")
                continue

            # Determine the maximum number of potions we can create with the current inventory
            max_potions = min(
                (red_ml // required_red if required_red > 0 else MAX_SAME_POTION),
                (green_ml // required_green if required_green > 0 else MAX_SAME_POTION),
                (blue_ml // required_blue if required_blue > 0 else MAX_SAME_POTION),
                (dark_ml // required_dark if required_dark > 0 else MAX_SAME_POTION),
                MAX_SAME_POTION
            )
            print(f"Maximum of {max_potions} '{name}' potions can be created based on current inventory.")

            # If we have abundant resources, create more potions
            potion_count = max_potions if any(inventory > RESOURCE_THRESHOLD for inventory in [red_ml, green_ml, blue_ml, dark_ml]) else 1

            if potion_count > 0:
                print(f"Planning to create {potion_count} of potion: {name}, SKU: {sku}")

                # Add to the bottle plan without actually updating the database
                bottle_plan.append({"potion_type": [required_red, required_green, required_blue, required_dark], "quantity": potion_count})

    print("Final bottle plan:", bottle_plan)
    return bottle_plan