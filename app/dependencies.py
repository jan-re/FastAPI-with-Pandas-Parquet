from attrs import define
import pandas as pd


@define
class FlightData():
    # aircraft: pd.DataFrame
    # aircraft_models: pd.DataFrame
    # airports: pd.DataFrame
    # carriers: pd.DataFrame
    # flights: pd.DataFrame

    # def __init__(self) -> None:
    #     self.aircraft = pd.read_parquet('./data/aircraft.parquet')
    #     self.aircraft_models = pd.read_parquet('./data/aircraft_models.parquet')
    #     self.airports = pd.read_parquet('./data/airports.parquet')
    #     self.carriers = pd.read_parquet('./data/carriers.parquet')
    #     self.flights = pd.read_parquet('./data/flights.parquet')

    def return_data(self) -> pd.DataFrame:
        return NotImplementedError

