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
    bottle_plan = []

    with db.engine.begin() as connection:
        # Query global_inventory
        sql_query = "SELECT num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory"
        result = connection.execute(sql_query)
        global_inventory = result.first()

        if global_inventory is None:
            print("No inventory found.")
            return bottle_plan

        inventory_red_ml, inventory_green_ml, inventory_blue_ml, inventory_dark_ml = global_inventory
        print(f"Inventory: red_ml: {inventory_red_ml}, green_ml: {inventory_green_ml}, blue_ml: {inventory_blue_ml}, dark_ml: {inventory_dark_ml}")

        # Query catalog for potion recipes
        sql_query = "SELECT sku, name, quantity, price, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml FROM catalog"
        catalog = connection.execute(sql_query).fetchall()

    for potion in catalog:
        sku, name, quantity, price, required_red, required_green, required_blue, required_dark = potion

        # Check if we have enough ingredients to make this potion
        can_create = (
            (required_red == 0 or inventory_red_ml >= required_red) and 
            (required_green == 0 or inventory_green_ml >= required_green) and 
            (required_blue == 0 or inventory_blue_ml >= required_blue) and 
            (required_dark == 0 or inventory_dark_ml >= required_dark)
        )

        if can_create:
            print(f"Creating potion: {name}, SKU: {sku}")

            # Add to the bottle plan
            bottle_plan.append({"potion_type": [required_red, required_green, required_blue, required_dark], "quantity": 1})

            # Update the inventory
            inventory_red_ml -= required_red
            inventory_green_ml -= required_green
            inventory_blue_ml -= required_blue
            inventory_dark_ml -= required_dark

            # Update the catalog with the new potion quantity
            with db.engine.begin() as connection:
                sql_query = "UPDATE catalog SET quantity = quantity + 1 WHERE sku = :sku"
                connection.execute(sql_query, {"sku": sku})

    # Update the global inventory after all potions are created
    with db.engine.begin() as connection:
        sql_query = "UPDATE global_inventory SET num_red_ml = :red_ml, num_green_ml = :green_ml, num_blue_ml = :blue_ml, num_dark_ml = :dark_ml"
        connection.execute(sql_query, {"red_ml": inventory_red_ml, "green_ml": inventory_green_ml, "blue_ml": inventory_blue_ml, "dark_ml": inventory_dark_ml})

    print("Final bottle plan:", bottle_plan)

    return bottle_plan