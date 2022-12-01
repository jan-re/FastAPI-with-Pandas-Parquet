import pandas as pd
import numpy as np
from typing import Any

class Flight_data():
    aircraft_models: dict[str, pd.DataFrame]
    aircraft: dict[str, pd.DataFrame]
    airports: dict[str, pd.DataFrame]
    carriers: dict[str, pd.DataFrame]
    flights: dict[str, pd.DataFrame]

    def __init__(self) -> None:
        self.aircraft = {'aircraft': pd.read_parquet('../data/aircraft.parquet')}
        self.aircraft_models = {'aircraft_models': pd.read_parquet('../data/aircraft_models.parquet')}
        self.airports = {'airports': pd.read_parquet('../data/airports.parquet')}
        self.carriers = {'carriers': pd.read_parquet('../data/carriers.parquet')}
        self.flights = {'flights': pd.read_parquet('../data/flights.parquet')}

        print('FAA data loaded successfully.')

    # TODO Unittest
    def get_all_datasets(self) -> list[dict[str, pd.DataFrame]]:
        return [self.aircraft, self.aircraft_models, self.airports, self.carriers, self.flights]

    # TODO Unittest
    def get_df_name(self, df: dict[str, pd.DataFrame]) -> str:
        keys = list(df.keys())
        return keys[0]

    # TODO Unittest
    def get_df_columns(self, df: pd.DataFrame) -> list[str]:
        return list(df.columns)

    # TODO Unittest
    def count_df_rows(self, df: pd.DataFrame) -> int:
        return len(df.index)

    # TODO Unittest
    def get_active_aircraft(self) -> pd.DataFrame:
        return self.aircraft['aircraft'].query('status_code == "A"', inplace=False)

    # TODO Unittest
    def get_filter_query(self, filter_by: dict[str, str | None]) -> str:
        cleared_filter_by: dict[str, str] = self.clear_filter_by(filter_by)
        filters: list[str] = []

        for key, value in cleared_filter_by.items():
            filters.append('({0} == "{1}")'.format(key, value))

        filter_query = ' & '.join(filters)

        return filter_query

    # TODO Unittest
    def clear_filter_by(self, filter_by: dict[str, str | None]) -> dict[str, str]:
        cleared_filter_by: dict[str,str] = {}

        for key, value in filter_by.items():
            if value is not None:
                cleared_filter_by[key] = value

        return cleared_filter_by

    # Needed for /datasets endpoint
    def list_loaded_datasets(self) -> str:
        datasets = self.get_all_datasets()
        dataset_specs: dict[str, list[Any]] = {'name': [], 'columns' : [], 'rowcount': []}

        for dataset in datasets:
            df_name = self.get_df_name(dataset)
            df = dataset[df_name]

            df_columns = self.get_df_columns(df)
            df_rowcount = self.count_df_rows(df)

            dataset_specs['name'].append(df_name)
            dataset_specs['columns'].append(df_columns)
            dataset_specs['rowcount'].append(df_rowcount)

        df = pd.DataFrame(dataset_specs)

        return df.to_csv(header=True, index=False)

    # Needed for /aircraft_models endpoint
    def list_aircraft_models(self) -> str:
        '''
        Retrieves all currently listed aircraft models from the available data and returns them in CSV form.

        Accepts no parameters.
        '''
        df: pd.DataFrame = self.aircraft_models['aircraft_models']
        df.sort_values(by=['model'])

        return df.to_csv(columns=['model', 'manufacturer', 'seats'], header=True, index=False)

    # Needed for /active_aircraft endpoint
    def list_active_aircraft(self, filter_by: dict[str, str | None]) -> str:
        df_aircraft_models = self.aircraft_models['aircraft_models']
        df_aircraft = self.get_active_aircraft()

        df_joined = df_aircraft.set_index('aircraft_model_code').join(df_aircraft_models.set_index('aircraft_model_code'), rsuffix='_2')

        filter_query = self.get_filter_query(filter_by)
        if filter_query:
            df_joined.query(filter_query, inplace=True)

        return df_joined.to_csv(columns=['manufacturer', 'model', 'seats', 'aircraft_serial', 'name', 'county'], header=True)

    def count_active_aircraft(self) -> Any:

        return NotImplemented