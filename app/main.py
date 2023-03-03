from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from .dependencies import FlightData

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


@app.get("/reports/modelsByState", tags=["reports"], status_code=200, response_class=PlainTextResponse)
async def read_models_by_state(response: str = Depends(flight_data.fetch_models_by_state)):
    return response


@app.get("/reports/modelsByStatePivot", tags=["reports"], status_code=200, response_class=PlainTextResponse)
async def read_models_by_state_pivot(response: str = Depends(flight_data.fetch_models_by_state_pivot)):
    return response
