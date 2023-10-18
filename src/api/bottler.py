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

    # Sort the catalog by the quantity, prioritizing potions with lesser quantity in stock.
    catalog = sorted(catalog, key=lambda x: x.quantity)

    # if all potions are already in stock
    if all(item.quantity != 0 for item in catalog):
        print("All potions are in stock.")
        return []

    # Try to create potions until we reach the plan limit or no more potions can be created.
    while len(bottle_plan) < 10:
        created_potion = False  # This flag checks if we've created a potion in this iteration.

        for item in catalog:
            sku, name, quantity, price, red_ml, green_ml, blue_ml, dark_ml = item

            # Print catalog item details
            print(f"Catalog Item - SKU: {sku}, Red: {red_ml}, Green: {green_ml}, Blue: {blue_ml}, Dark: {dark_ml}, Quantity: {quantity}, Price: {price}")

            # Check if we have enough materials in inventory to create this potion.
            if (red_ml == 0 or inventory_red_ml >= red_ml) and \
               (green_ml == 0 or inventory_green_ml >= green_ml) and \
               (blue_ml == 0 or inventory_blue_ml >= blue_ml) and \
               (dark_ml == 0 or inventory_dark_ml >= dark_ml):

                print(f"Creating potion: {name}, SKU: {sku}")

                # Add the potion to the plan and update the inventory.
                bottle_plan.append({"potion_type": [int(red_ml > 0), int(green_ml > 0), int(blue_ml > 0), int(dark_ml > 0)], "quantity": 1})
                inventory_red_ml -= red_ml
                inventory_green_ml -= green_ml
                inventory_blue_ml -= blue_ml
                inventory_dark_ml -= dark_ml

                created_potion = True

                # If we created a potion, let's move to the next iteration to check other potions or inventory constraints.
                break  

        # If we didn't create any potion during this full pass on the catalog, or if the bottle plan is full, we exit the loop.
        if not created_potion or len(bottle_plan) == 10:
            break

    # Update global_inventory after all potions have been planned.
    with db.engine.begin() as connection:
        sql_query = """UPDATE global_inventory SET num_red_ml = :red_ml, num_green_ml = :green_ml, num_blue_ml = :blue_ml, num_dark_ml = :dark_ml"""
        connection.execute(sqlalchemy.text(sql_query), {"red_ml": inventory_red_ml, "green_ml": inventory_green_ml, "blue_ml": inventory_blue_ml, "dark_ml": inventory_dark_ml})

    print("Final bottle plan:", bottle_plan)

    return bottle_plan