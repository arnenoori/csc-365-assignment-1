from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

class Result(BaseModel):
    gold_match: bool
    barrels_match: bool
    potions_match: bool

@router.get("/inventory")
def get_inventory():
    """ """
    with db.engine.begin() as connection:
        sql_query = """
        SELECT 
            (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'gold') AS gold,
            (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'red_ml') AS ml_in_red_barrels,
            (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'green_ml') AS ml_in_green_barrels,
            (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'blue_ml') AS ml_in_blue_barrels,
            (SELECT SUM(change) FROM inventory_ledger_entries WHERE inventory_type = 'dark_ml') AS ml_in_dark_barrels
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        first_row = result.first()

    if first_row is None:
        return {
            "gold": 100,
            "ml_in_red_barrels": 0,
            "ml_in_green_barrels": 0,
            "ml_in_blue_barrels": 0,
            "ml_in_dark_barrels": 0
        }

    return {
        "gold": first_row.gold,
        "ml_in_red_barrels": first_row.ml_in_red_barrels,
        "ml_in_green_barrels": first_row.ml_in_green_barrels,
        "ml_in_blue_barrels": first_row.ml_in_blue_barrels,
        "ml_in_dark_barrels": first_row.ml_in_dark_barrels
    }

@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"