from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewCart(BaseModel):
    customer: str

@router.post("/")
def create_cart(new_cart: NewCart):
    with db.engine.begin() as connection:
        sql_query = f"""
        INSERT INTO carts (customer)
        VALUES ('{new_cart.customer}')
        RETURNING id
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        cart_id = result.first()[0]

    return {"cart_id": cart_id}

@router.get("/{cart_id}")
def get_cart(cart_id: int):
    with db.engine.begin() as connection:
        sql_query = f"""
        SELECT * FROM carts
        WHERE id = {cart_id}
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        cart = result.first()

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

class CartItem(BaseModel):
    quantity: int

@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    with db.engine.begin() as connection:
        sql_query = f"""
        UPDATE cart_items
        SET quantity = {cart_item.quantity}
        WHERE cart_id = {cart_id} AND item_sku = '{item_sku}'
        """
        connection.execute(sqlalchemy.text(sql_query))

    return "OK"

class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    with db.engine.begin() as connection:
        # Fetch all items in the cart
        sql_query = f"""
        SELECT item_sku, quantity
        FROM cart_items
        WHERE cart_id = {cart_id}
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        cart_items = result.fetchall()

        # For each item in the cart, decrease the inventory
        for item in cart_items:
            sql_query = f"""
            UPDATE global_inventory
            SET num_red_potions = num_red_potions - {item.quantity}
            WHERE sku = '{item.item_sku}'
            """
            connection.execute(sqlalchemy.text(sql_query))

        # Calculate the total price
        sql_query = f"""
        SELECT SUM(quantity * price) as total
        FROM cart_items
        JOIN items ON cart_items.item_sku = items.sku
        WHERE cart_id = {cart_id}
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        total = result.first()[0]

        if total > cart_checkout.payment:
            raise HTTPException(status_code=400, detail="Insufficient payment")

        # Update the gold in the global_inventory table
        sql_query = f"""
        UPDATE global_inventory
        SET gold = gold + {cart_checkout.payment}
        """
        connection.execute(sqlalchemy.text(sql_query))

    return {"total_potions_bought": total, "total_gold_paid": cart_checkout.payment}