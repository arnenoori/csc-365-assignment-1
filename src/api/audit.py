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
        sql_query = """SELECT num_red_potions, num_red_ml, gold from global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        first_row = result.first()

    return {"number_of_red_potions": first_row.num_red_potions, "ml_in_red_barrels": first_row.num_red_ml, "gold": first_row.gold}

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"