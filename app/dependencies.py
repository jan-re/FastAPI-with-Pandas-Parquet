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

    def return_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict({
            "name": self.name,
            "columns": [self.columns],
            "length": self.length
        })


@define
class FlightData():
    aircraft: pd.DataFrame
    models: pd.DataFrame
    airports: pd.DataFrame
    carriers: pd.DataFrame
    flights: pd.DataFrame
    handler: Handler

    def __init__(self) -> None:
        self.handler = Handler()

    def load_data(self) -> None:
        self.aircraft = pd.read_parquet("./app//data/aircraft.parquet")
        self.models = pd.read_parquet("./app/data/aircraft_models.parquet")
        self.airports = pd.read_parquet("./app/data/airports.parquet")
        self.carriers = pd.read_parquet("./app/data/carriers.parquet")
        self.flights = pd.read_parquet("./app/data/flights.parquet")

        print("INFO:     Flight data loaded!")

    def join_aircraft_and_models(self) -> pd.DataFrame:
        return self.aircraft.set_index("aircraft_model_code").join(self.models.set_index("aircraft_model_code"), rsuffix="_2")

    def fetch_datasets(self) -> str:
        return self.handler.handle_datasets(self)

    def fetch_models(self) -> str:
        return self.handler.handle_models(self.models)

    def fetch_active_aircraft(self, manufacturer: str | None = None, model: str | None = None) -> str:
        return self.handler.handle_active_aircraft(self.join_aircraft_and_models(), manufacturer, model)

    def fetch_models_by_county(self) -> str:
        return self.handler.handle_models_by_county(self.join_aircraft_and_models())


@define
class Handler():

    def handle_datasets(self, data: FlightData) -> str:
        datasets: list[DatasetStats] = []

        datasets.append(DatasetStats("aircraft", list(data.aircraft.columns), len(data.aircraft.index)))
        datasets.append(DatasetStats("aircraft_models", list(data.models.columns), len(data.models.index)))
        datasets.append(DatasetStats("airports", list(data.airports.columns), len(data.airports.index)))
        datasets.append(DatasetStats("carriers", list(data.carriers.columns), len(data.carriers.index)))
        datasets.append(DatasetStats("flights", list(data.flights.columns), len(data.flights.index)))

        response = pd.DataFrame(columns=["name", "columns", "length"])

        for dt in datasets:
            df = dt.return_dataframe()
            response = pd.concat([response, df], ignore_index=True)

        return response.to_csv(header=True, index=False)

    def handle_models(self, data: pd.DataFrame) -> str:
        return data.to_csv(
            columns=["model", "manufacturer", "seats"],
            header=True,
            index=False
        )

    def handle_active_aircraft(self, data: pd.DataFrame, manufacturer: str | None, model: str | None) -> str:
        response = data.query("status_code == \"A\"", inplace=False)

        if manufacturer:
            response = response.query(f"manufacturer == \"{manufacturer}\"", inplace=False)

        if model:
            response = response.query(f"model == \"{model}\"", inplace=False)

        return response.to_csv(
            columns=["manufacturer", "model", "seats", "aircraft_serial", "name", "county"],
            header=True,
            index=False
        )

    def handle_models_by_county(self, data: pd.DataFrame) -> str:
        response = data.query("status_code == \"A\"", inplace=False)

        # CONTINUE FROM HERE
        #response = response.groupby(["county

        # Count aircraft, manufacturer by county

        return data.to_csv(
            columns=["manufacturer", "model", "seats", "aircraft_serial", "name", "county"],
            header=True,
            index=False
        )
    

    """
    Return summary counts of active aircraft models and their manufacturer by the county in
    which those aircrafts are registered.

    All data needed for this endpoint is in the aircraft and aircraft_models data
    files.
    """
