from fastapi import APIRouter, Depends
from enum import Enum
from typing import List
from pydantic import BaseModel
from src.api import auth
from src import database as db
from sqlalchemy import text
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

            # Update catalog
            sql_query = """
            INSERT INTO catalog (sku, name, quantity, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml)
            VALUES (:sku, :name, :quantity, :red_ml, :green_ml, :blue_ml, :dark_ml) 
            ON CONFLICT (sku) DO UPDATE 
            SET quantity = catalog.quantity + :quantity
            WHERE catalog.quantity + :quantity <= 10000  -- This ensures the quantity does not exceed the maximum
            """
            connection.execute(sqlalchemy.text(sql_query), {
                "sku": sku, 
                "name": name, 
                "quantity": quantity, 
                "red_ml": red_ml, 
                "green_ml": green_ml, 
                "blue_ml": blue_ml, 
                "dark_ml": dark_ml
            })

            print(f"Updated catalog with potion: {potion}")

            # Update global_inventory
            sql_query = """
            UPDATE global_inventory SET 
                num_red_ml = num_red_ml - :red_ml,
                num_green_ml = num_green_ml - :green_ml,
                num_blue_ml = num_blue_ml - :blue_ml,
                num_dark_ml = num_dark_ml - :dark_ml
            """
            connection.execute(sqlalchemy.text(sql_query), {
                "red_ml": red_ml * quantity, 
                "green_ml": green_ml * quantity, 
                "blue_ml": blue_ml * quantity, 
                "dark_ml": dark_ml * quantity
            })

            print(f"Updated global_inventory with potion: {potion}")

    print("Finished delivery of potions.")
    return "OK"

@router.post("/plan")
def get_bottle_plan():
    MAX_SAME_POTION = 10  # The maximum number of the same potions to create at once
    RESOURCE_THRESHOLD = 2000  # The threshold above which we create up to 10 potions, so we keep 1000 ml for mixed potions
    bottle_plan = []

    with db.engine.begin() as connection:
        # Query global_inventory
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
        result = connection.execute(text(sql_query))
        global_inventory = result.first()

        if global_inventory is None:
            print("No inventory found.")
            return bottle_plan

        inventory_red_ml, inventory_green_ml, inventory_blue_ml, inventory_dark_ml = global_inventory
        print(f"Inventory: red_ml: {inventory_red_ml}, green_ml: {inventory_green_ml}, blue_ml: {inventory_blue_ml}, dark_ml: {inventory_dark_ml}")

        # Query catalog for potion recipes
        sql_query = """SELECT sku, name, quantity, price, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM catalog"""
        catalog = connection.execute(text(sql_query)).fetchall()

    for potion in catalog:
        sku, name, quantity, price, required_red, required_green, required_blue, required_dark = potion

        # Check if we have enough ingredients for at least one potion
        can_create = all([
            inventory_red_ml >= required_red if required_red > 0 else True,
            inventory_green_ml >= required_green if required_green > 0 else True,
            inventory_blue_ml >= required_blue if required_blue > 0 else True,
            inventory_dark_ml >= required_dark if required_dark > 0 else True
        ])

        if not can_create:
            print(f"Not enough inventory to create even one '{name}'. Skipping...")
            continue # Skip this potion if there's not enough inventory for any type to make sure I can't get negative ML

        # Determine the maximum number of potions we can create with the current inventory
        max_potions = min(
            (inventory_red_ml // required_red if required_red > 0 else MAX_SAME_POTION),
            (inventory_green_ml // required_green if required_green > 0 else MAX_SAME_POTION),
            (inventory_blue_ml // required_blue if required_blue > 0 else MAX_SAME_POTION),
            (inventory_dark_ml // required_dark if required_dark > 0 else MAX_SAME_POTION),
            MAX_SAME_POTION  # Ensure we don't create more than the maximum allowed number of the same potion
        )
        print(f"Maximum of {max_potions} '{name}' potions can be created based on current inventory.")

        # If we have abundant resources (e.g., more than 2000 ml), create more potions (up to 10)
        if max_potions > 0 and any(inventory > RESOURCE_THRESHOLD for inventory in [inventory_red_ml, inventory_green_ml, inventory_blue_ml, inventory_dark_ml]):
            potion_count = max_potions
        else:
            potion_count = 1  # default to creating one potion if resources are not abundant

        if potion_count > 0:
            print(f"Creating {potion_count} of potion: {name}, SKU: {sku}")

            # Add to the bottle plan
            bottle_plan.append({"potion_type": [required_red, required_green, required_blue, required_dark], "quantity": potion_count})

            # Update the inventory
            inventory_red_ml -= required_red * potion_count
            inventory_green_ml -= required_green * potion_count
            inventory_blue_ml -= required_blue * potion_count
            inventory_dark_ml -= required_dark * potion_count

            # Update the catalog with the new potion quantity
            with db.engine.begin() as connection:
                sql_query = """UPDATE catalog SET quantity = quantity + :new_quantity WHERE sku = :sku"""
                connection.execute(text(sql_query), {"sku": sku, "new_quantity": potion_count})

    # Update the global inventory after all potions are created
    with db.engine.begin() as connection:
        sql_query = """UPDATE global_inventory SET num_red_ml = :red_ml, num_green_ml = :green_ml, num_blue_ml = :blue_ml, num_dark_ml = :dark_ml"""
        connection.execute(text(sql_query), {"red_ml": inventory_red_ml, "green_ml": inventory_green_ml, "blue_ml": inventory_blue_ml, "dark_ml": inventory_dark_ml})

    print("Final bottle plan:", bottle_plan)

    return bottle_plan