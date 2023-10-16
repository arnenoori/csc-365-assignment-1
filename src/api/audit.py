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
        sql_query = """SELECT gold, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml from global_inventory"""
        result = connection.execute(sqlalchemy.text(sql_query))
        first_row = result.first()

    return {
        "gold": first_row.gold,
        "ml_in_red_barrels": first_row.num_red_ml,
        "ml_in_green_barrels": first_row.num_green_ml,
        "ml_in_blue_barrels": first_row.num_blue_ml,
        "ml_in_dark_barrels": first_row.num_dark_ml
    }

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"