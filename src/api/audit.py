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
        # Fetch inventory details
        sql_query = """SELECT potion_id, quantity, ml FROM global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        inventory = [dict(row) for row in result.fetchall()]
        # Fetch quantity of each potion
        sql_query = """SELECT id, name, quantity FROM potions"""
        result = connection.execute(sqlalchemy.text(sql_query))
        potions = [dict(row) for row in result.fetchall()]

    return {"inventory": inventory, "potions": potions}

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"