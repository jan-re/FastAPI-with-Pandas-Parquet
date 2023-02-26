from fastapi import Depends, FastAPI
from .routers import entities, reports
from .dependencies import FlightData

app = FastAPI()

flight_data: FlightData = FlightData()


app.include_router(
    entities.router,
    dependencies=[Depends(flight_data.return_data())]
)

app.include_router(
    reports.router,
    dependencies=[Depends(flight_data.return_data())]
)
