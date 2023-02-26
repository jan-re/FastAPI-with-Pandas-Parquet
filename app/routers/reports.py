from fastapi import APIRouter
from pydantic import BaseModel


class Query(BaseModel):
    query: str


router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.get("/modelsByCounty", status_code=200)
async def read_models_by_county():
    return NotImplementedError


@router.get("/modelsByCountyPivot", status_code=200)
async def read_models_by_county_pivot():
    return NotImplementedError


@router.post("/customReport", status_code=200)
async def create_sql_report(query: Query):
    return NotImplementedError
