from fastapi import Depends, FastAPI
from pydantic import BaseModel
from .dependencies import FlightData


class Query(BaseModel):
    query: str


app = FastAPI()

flight_data: FlightData = FlightData()


@app.on_event("startup")
def startup_load():
    flight_data.load_data()


@app.get("/entities/datasets", tags=["entities"], status_code=200)
async def read_datasets(data: str = Depends(flight_data.fetch_datasets)):
    """
    Clients can get information about the loaded data sets. For each of the FAA data file, service returns:
    - Name of the data file
    - List of columns
    - Total number of rows
    """
    return NotImplemented


@app.get("/entities/models", tags=["entities"], status_code=200)
async def read_models(data: str = Depends(flight_data.fetch_models)):
    """
    Client can call with no parameters and that will return all known aircraft models, their manufacturer and number of seats.
    All data needed for this endpoint is in the aircraft_models data file.
    """
    return NotImplemented


@app.get("/entities/activeAircraft", tags=["entities"], status_code=200)
async def read_active_aircraft(manufacturer: str | None = None, model: str | None = None, data: str = Depends(flight_data.fetch_active_aircraft)):
    """
    Client can call with two parameters:
    - Aircraft manufacturer
    - Aircraft model
    Given this input, your service must return all active aircrafts of the selected model and manufacturer. For each found aircraft, the endpoint must return:
    - Manufacturer
    - Model,
    - Number of seats
    - Serial number
    - Registrant name
    - Registrant county
    All data needed for this endpoint is in the aircraft and aircraft_models data files.
    """
    return NotImplemented


#@app.get("/reports/modelsByCounty", tags=["reports"], status_code=200)
#async def read_models_by_county(data: str = Depends(flight_data.fetch_datasets)):
#    return NotImplemented
#
#
#@app.get("/reports/modelsByCountyPivot", tags=["reports"], status_code=200)
#async def read_models_by_county_pivot(data: str = Depends(flight_data.fe)):
#    return NotImplemented
#
#
#@app.post("/reports/customReport", tags=["reports"], status_code=200)
#async def create_sql_report(query: Query):
#    return NotImplemented
