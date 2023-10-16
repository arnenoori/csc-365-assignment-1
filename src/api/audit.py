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
    with db.engine.begin() as connection:
        sql_query = """
        SELECT i.id, SUM(ile.change) AS quantity
        FROM global_inventory i
        JOIN inventory_ledger_entries ile ON i.id = ile.inventory_id
        GROUP BY i.id;
        """
        result = connection.execute(sqlalchemy.text(sql_query))
        inventory = result.fetchall()

    return inventory

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"