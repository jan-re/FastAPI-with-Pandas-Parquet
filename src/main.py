import pandas as pd
import numpy as np
from typing import cast

class Flight_data():
    aircraft_models: dict[str, str | pd.DataFrame]
    aircraft: dict[str, str | pd.DataFrame]
    airports: dict[str, str | pd.DataFrame]
    carriers: dict[str, str | pd.DataFrame]
    flights: dict[str, str | pd.DataFrame]

    def __init__(self) -> None:
        self.aircraft = { 'name': 'aircraft', 'data': pd.read_parquet('../data/aircraft.parquet')}
        self.aircraft_models = { 'name': 'aircraft_models', 'data': pd.read_parquet('../data/aircraft_models.parquet')}
        self.airports = { 'name': 'airports', 'data': pd.read_parquet('../data/airports.parquet')}
        self.carriers = { 'name': 'carriers', 'data': pd.read_parquet('../data/carriers.parquet')}
        self.flights = { 'name': 'flights', 'data': pd.read_parquet('../data/flights.parquet')}

        print('FAA data loaded successfully.')

    def get_all_dataframes(self) -> list[dict[str, str | pd.DataFrame]]:
        return [self.aircraft, self.aircraft_models, self.airports, self.carriers, self.flights]

    def get_dataframe_name(self, df: dict[str, str | pd.DataFrame]) -> str:
        name = df['name']
        return cast(str, name)

    def get_columns(self, df: pd.DataFrame) -> list[str]:
        return list(df.columns)

    # Needed for /datasets endpoint
    def list_datasets(self) -> list[list[str]]:
        dfs = self.get_all_dataframes()

        for df in dfs:
            print('For: ' + self.get_dataframe_name(df))
            print('Columns: ' + self.get_columns(df))

        return [['hello'], ['there']]

    # Needed for /aircraft_models endpoint
    def list_aircraft_models(self) -> list[list[str]]:

        return [['hello'], ['there']]

    # Needed for /active_aircraft endpoint
    def list_active_aircraft(self, manufacturer: str, model: str) -> list[list[str]]:

        return [['hello'], ['there']]

    def count_active_aircraft(self) -> list[list[int]]:

        return [[1]]


data = Flight_data()


data.list_datasets()
