from fastapi import APIRouter, Depends
from enum import Enum
from typing import List
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

        for potion in potions_delivered:
            print(f"Processing potion: {potion}")
            if len(potion.potion_type) != 4:
                print(f"Error: potion.potion_type must contain exactly four elements, but got {len(potion.potion_type)}.")
                continue

            red_ml, green_ml, blue_ml, dark_ml = potion.potion_type
            sku = name = f"{red_ml}_{green_ml}_{blue_ml}_{dark_ml}"
            quantity = potion.quantity

            # Determine id from catalog based on sku
            for item in catalog:
                if item.sku == sku:
                    id = item.id
                    break
            else:
                id = None

            # Update catalog
            sql_query = """
            INSERT INTO catalog (id, sku, name, price, quantity, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml)
            VALUES (:id, :sku, :name, :price, :quantity, :red_ml, :green_ml, :blue_ml, :dark_ml) 
            ON CONFLICT (id) DO UPDATE SET quantity = catalog.quantity + :quantity
            """
            connection.execute(sqlalchemy.text(sql_query), {
                "id": id, 
                "sku": sku, 
                "name": name, 
                "price": 1, 
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
                num_red_ml = num_red_ml + :red_ml,
                num_green_ml = num_green_ml + :green_ml,
                num_blue_ml = num_blue_ml + :blue_ml,
                num_dark_ml = num_dark_ml + :dark_ml
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
    """
    Go from barrel to bottle. Gets called 4 times a day
    """
    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.
    bottle_plan = []
    with db.engine.begin() as connection:
        # Query global_inventory
        sql_query = """SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        global_inventory = result.first()

        if global_inventory is None:
            print("No inventory found.")
            return bottle_plan

        inventory_red_ml, inventory_green_ml, inventory_blue_ml, inventory_dark_ml = global_inventory
        print(f"Inventory: red_ml: {inventory_red_ml}, green_ml: {inventory_green_ml}, blue_ml: {inventory_blue_ml}, dark_ml: {inventory_dark_ml}")

    # Query catalog outside of the previous connection block
    with db.engine.begin() as connection:
        sql_query = """SELECT sku, name, quantity, price, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM catalog"""
        catalog = connection.execute(sqlalchemy.text(sql_query)).fetchall()
    catalog = sorted(catalog, key=lambda x: x.quantity)

    # if all potions already in stock
    if all(item.quantity != 0 for item in catalog):
        print("All potions are in stock.")
        return []

    while len(bottle_plan) < 6:  # Limit the bottle_plan to max 6 items
        updated = False  # Flag to check if any potion was created in this iteration
        for item in catalog:
            sku, name, quantity, price, red_ml, green_ml, blue_ml, dark_ml = item

            if (inventory_red_ml >= red_ml) and (inventory_green_ml >= green_ml) and (inventory_blue_ml >= blue_ml) and (inventory_dark_ml >= dark_ml):
                print(f"Creating potion: {name}, SKU: {sku}")
                bottle_plan.append({"potion_type": [red_ml, green_ml, blue_ml, dark_ml], "quantity": 1})

                inventory_red_ml -= red_ml
                inventory_green_ml -= green_ml
                inventory_blue_ml -= blue_ml
                inventory_dark_ml -= dark_ml

                updated = True
                break  # Break after one potion is created to re-evaluate the next potion with the updated inventory

        if not updated or len(bottle_plan) == 6:  # If no potion was created or bottle_plan is full, break the loop
            break

    # Update global_inventory after all the potions have been created
    with db.engine.begin() as connection:
        sql_query = """UPDATE global_inventory SET num_red_ml = :red_ml, num_green_ml = :green_ml, num_blue_ml = :blue_ml, num_dark_ml = :dark_ml"""
        connection.execute(sqlalchemy.text(sql_query), {"red_ml": inventory_red_ml, "green_ml": inventory_green_ml, "blue_ml": inventory_blue_ml, "dark_ml": inventory_dark_ml})

    print("Final bottle plan:", bottle_plan)

    return bottle_plan