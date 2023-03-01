from __future__ import annotations
from attrs import define
import pandas as pd


@define
class DatasetStats():
    name: str
    columns: list[str]
    length: int

    def __init__(self, name, columns, length) -> None:
        self.name = name
        self.columns = columns
        self.length = length


@define
class FlightData():
    aircraft: pd.DataFrame
    aircraft_models: pd.DataFrame
    airports: pd.DataFrame
    carriers: pd.DataFrame
    flights: pd.DataFrame
    handler: Handler

    def __init__(self) -> None:
        self.handler = Handler()

    def load_data(self) -> None:
        self.aircraft = pd.read_parquet('./app//data/aircraft.parquet')
        self.aircraft_models = pd.read_parquet('./app/data/aircraft_models.parquet')
        self.airports = pd.read_parquet('./app/data/airports.parquet')
        self.carriers = pd.read_parquet('./app/data/carriers.parquet')
        self.flights = pd.read_parquet('./app/data/flights.parquet')

        print("Flight data loaded.")

    def fetch_datasets(self) -> str:
        return self.handler.handle_datasets(self)

    def fetch_models(self) -> str:
        return self.handler.handle_models(self.aircraft_models)

    def fetch_active_aircraft(self, manufacturer: str | None, model: str | None) -> str:
        return self.handler.handle_active_aircraft(self.aircraft, self.aircraft_models, manufacturer, model)


@define
class Handler():

    def handle_datasets(self, flight_data: FlightData) -> str:

        aircraft = DatasetStats("aircraft", list(flight_data.aircraft.columns), len(flight_data.aircraft.index))
        aircraft_models = DatasetStats("aircraft_models", list(flight_data.aircraft_models.columns), len(flight_data.aircraft_models.index))
        airports = DatasetStats("airports", list(flight_data.airports.columns), len(flight_data.airports.index))
        carriers = DatasetStats("carriers", list(flight_data.carriers.columns), len(flight_data.carriers.index))
        flights = DatasetStats("flights", list(flight_data.flights.columns), len(flight_data.flights.index))

        # Continue from here

        return NotImplemented
    
    def handle_models(self, aircraft_models: pd.DataFrame) -> str:
        return NotImplemented

    def handle_active_aircraft(self, aircraft: pd.DataFrame, aircraft_models: pd.DataFrame, manufacturer: str | None, model: str | None) -> str:
        return NotImplemented
