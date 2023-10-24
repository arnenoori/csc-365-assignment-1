from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy
from enum import Enum


router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

class search_sort_options(str, Enum):
    customer_name = "customer_name"
    item_sku = "item_sku"
    line_item_total = "line_item_total"
    timestamp = "timestamp"

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

@router.get("/search/", tags=["search"])
def search_orders(
    customer_name: str = "",
    potion_sku: str = "",
    search_page: str = "",
    sort_col: search_sort_options = search_sort_options.timestamp,
    sort_order: search_sort_order = search_sort_order.desc,
):
    """
    Search for cart line items by customer name and/or potion sku.

    Customer name and potion sku filter to orders that contain the 
    string (case insensitive). If the filters aren't provided, no
    filtering occurs on the respective search term.

    Search page is a cursor for pagination. The response to this
    search endpoint will return previous or next if there is a
    previous or next page of results available. The token passed
    in that search response can be passed in the next search request
    as search page to get that page of results.

    Sort col is which column to sort by and sort order is the direction
    of the search. They default to searching by timestamp of the order
    in descending order.
psql
    The response itself contains a previous and next page token (if
    such pages exist) and the results as an array of line items. Each
    line item contains the line item id (must be unique), item sku, 
    customer name, line item total (in gold), and timestamp of the order.
    Your results must be paginated, the max results you can return at any
    time is 5 total line items.
    """
    # Construct SQL query based on filter, sort, page, and page_size
    sql_query = f"""
    SELECT carts.id, carts.customer, cart_items.item_sku, cart_items.quantity
    FROM carts
    LEFT JOIN cart_items ON carts.id = cart_items.cart_id
    WHERE carts.customer LIKE '%{customer_name}%' AND cart_items.item_sku LIKE '%{potion_sku}%'
    ORDER BY {sort_col} {sort_order}
    LIMIT 5 OFFSET {int(search_page) * 5}
    """

    # Execute SQL query and fetch results
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_query))
        results = [row._asdict() for row in result]

    # Format results into JSON response
    response = {
        "previous": str(max(0, int(search_page) - 1)),
        "next": str(int(search_page) + 1),
        "results": results,
    }

    return response


class NewCart(BaseModel):
    customer: str

@router.post("/")
def create_cart(new_cart: NewCart):
    print("Creating a new cart...")
    with db.engine.begin() as connection:
        sql_query = f"""
        INSERT INTO carts (customer)
        VALUES ('{new_cart.customer}')
        RETURNING id
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        cart_id = result.first()[0]

    print(f"Created a new cart with id: {cart_id}")
    return {"cart_id": cart_id}

@router.get("/{cart_id}")
def get_cart(cart_id: int):
    print(f"Getting cart with id: {cart_id}")
    with db.engine.begin() as connection:
        sql_query = f"""
        SELECT carts.id, carts.customer, cart_items.item_sku, cart_items.quantity
        FROM carts
        LEFT JOIN cart_items ON carts.id = cart_items.cart_id
        WHERE carts.id = {cart_id}
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        cart = [row._asdict() for row in result]

        if not cart:
            print(f"Cart with id: {cart_id} not found")
            raise HTTPException(status_code=404, detail="Cart not found")
        
    print(f"Returning cart: {cart}")
    return cart

class CartItem(BaseModel):
    item_sku: str
    quantity: int

@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    print(f"Setting item quantity for cart_id: {cart_id}, item_sku: {item_sku}")
    with db.engine.begin() as connection:
        # Check if the item already exists in the cart
        sql_query = f"""
        SELECT 1 FROM cart_items
        WHERE cart_id = {cart_id} AND item_sku = '{item_sku}'
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        item_exists = result.scalar() is not None

        if item_exists:
            # If the item exists, update the quantity
            print(f"Item exists in the cart, updating quantity to: {cart_item.quantity}")
            sql_query = f"""
            UPDATE cart_items
            SET quantity = {cart_item.quantity}
            WHERE cart_id = {cart_id} AND item_sku = '{item_sku}'
            """
        else:
            # If the item doesn't exist, insert a new record
            print(f"Item does not exist in the cart, inserting new record with quantity: {cart_item.quantity}")
            sql_query = f"""
            INSERT INTO cart_items (cart_id, item_sku, quantity)
            VALUES ({cart_id}, '{item_sku}', {cart_item.quantity})
            """

        connection.execute(sqlalchemy.text(sql_query))

    print("Item quantity set successfully")
    return "OK"

class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    print(f"Checking out cart with id: {cart_id}")
    with db.engine.begin() as connection:
        # Get the items in the cart
        sql_query = """
        SELECT item_sku, quantity
        FROM cart_items
        WHERE cart_id = :cart_id
        """
        result = connection.execute(sqlalchemy.text(sql_query), {"cart_id": cart_id})
        cart_items = result.fetchall()

        total_gold_paid = 0
        total_potions_bought = 0

        for item_sku, quantity in cart_items:
            # Get price from catalog, add to total gold paid
            sql_query = """
            SELECT price
            FROM catalog
            WHERE sku = :item_sku
            """
            result = connection.execute(sqlalchemy.text(sql_query), {"item_sku": item_sku})
            item = result.first()
            if item is None:
                print(f"Item with SKU {item_sku} not found in catalog")
                raise HTTPException(status_code=404, detail=f"Item with SKU {item_sku} not found in catalog")
            total_gold_paid += item.price * quantity
            total_potions_bought += quantity

            # Decrease quantity in catalog table
            sql_query = """
            UPDATE catalog
            SET quantity = quantity - :quantity
            WHERE sku = :item_sku
            """
            connection.execute(sqlalchemy.text(sql_query), {"quantity": quantity, "item_sku": item_sku})

            # Remove items from cart_items
            sql_query = """
            DELETE FROM cart_items
            WHERE cart_id = :cart_id AND item_sku = :item_sku
            """
            connection.execute(sqlalchemy.text(sql_query), {"cart_id": cart_id, "item_sku": item_sku})

        # Create a new transaction for the checkout
        sql_query = """
        INSERT INTO inventory_transactions (description)
        VALUES (:description)
        RETURNING id
        """
        transaction_id = connection.execute(sqlalchemy.text(sql_query), {"description": "Checkout cart"}).scalar()

        # Create ledger entry for the gold paid
        sql_query = """
        INSERT INTO inventory_ledger_entries (inventory_id, transaction_id, change)
        VALUES (:inventory_id, :transaction_id, :change)
        """
        connection.execute(sqlalchemy.text(sql_query), {"inventory_id": 1, "transaction_id": transaction_id, "change": total_gold_paid})

    print(f"Checkout successful. Total potions bought: {total_potions_bought}, Total gold paid: {total_gold_paid}")
    return {"total_potions_bought": total_potions_bought, "total_gold_paid": total_gold_paid}