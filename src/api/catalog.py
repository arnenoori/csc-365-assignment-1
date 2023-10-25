from fastapi import APIRouter, HTTPException
from src import database as db
import sqlalchemy

router = APIRouter()

@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    catalog = []
    try:
        # Fetch the catalog from the database
        with db.engine.begin() as connection:
            sql_query = """
                SELECT c.sku, c.name, SUM(ile.change), c.price, c.num_red_ml, c.num_green_ml, c.num_blue_ml, c.num_dark_ml 
                FROM catalog c
                LEFT JOIN inventory_ledger_entries ile ON c.id = ile.transaction_id
                GROUP BY c.sku, c.name, c.price, c.num_red_ml, c.num_green_ml, c.num_blue_ml, c.num_dark_ml
            """
            result = connection.execute(sqlalchemy.text(sql_query))
            catalog = result.fetchall()

        # Convert the catalog to the required format
        catalog = [{
            "sku": row[0],
            "name": row[1],
            "quantity": row[2],
            "price": row[3],
            "potion_type": [row[4], row[5], row[6], row[7]],  # constructing array in Python
        } for row in catalog]

    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)  # Log the error message
        raise HTTPException(status_code=500, detail="Internal server error")

    return catalog