from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from .dependencies import FlightData


class Query(BaseModel):
    query: str


app = FastAPI()

flight_data: FlightData = FlightData()


@app.on_event("startup")
def startup_load():
    flight_data.load_data()


@app.get("/entities/datasets", tags=["entities"], status_code=200, response_class=PlainTextResponse)
async def read_datasets(response: str = Depends(flight_data.fetch_datasets)):
    return response


@app.get("/entities/models", tags=["entities"], status_code=200, response_class=PlainTextResponse)
async def read_models(response: str = Depends(flight_data.fetch_models)):
    return response


@app.get("/entities/activeAircraft", tags=["entities"], status_code=200, response_class=PlainTextResponse)
async def read_active_aircraft(response: str = Depends(flight_data.fetch_active_aircraft)):
    return response


@app.get("/reports/modelsByCounty", tags=["reports"], status_code=200, response_class=PlainTextResponse)
async def read_models_by_county(response: str = Depends(flight_data.fetch_models_by_county)):
    return response


# @app.get("/reports/modelsByCountyPivot", tags=["reports"], status_code=200)
# async def read_models_by_county_pivot(data: str = Depends(flight_data.fetch)):
#     return NotImplemented

#
#
#@app.post("/reports/customReport", tags=["reports"], status_code=200)
#async def create_sql_report(query: Query):
#    return NotImplemented

