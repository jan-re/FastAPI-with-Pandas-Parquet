import pandas as pd
from typing import Any


class FlightData():
    """
    FlightData handles loading data from the pre-defined parquet files when initialised. They are loaded into the class attributes named *_data, where * denotes the name of the parquet file.

    They are stored in a dict that contains its name as a string and the actual data as a pd.DataFrame.\
        The class itself contains function definitions that work with the DataFrames according to the homework instructions.\
        Functions starting with list_* serve to output CSV data as str type. That data is ultimately sent over API elsewhere in the program.
    """
    aircraft_models_data: dict[str, pd.DataFrame]
    aircraft_data: dict[str, pd.DataFrame]
    airports_data: dict[str, pd.DataFrame]
    carriers_data: dict[str, pd.DataFrame]
    flights_data: dict[str, pd.DataFrame]

    def __init__(self) -> None:
        """
        Note that the path to the data is hardcoded and not open to user input. If there's any changes in the file structure, it needs to be reflected here as well.\
            If the path is wrong, the application will crash. This is acceptable, as there's no point in running it without the data.

        WouldBeNice: Accept user input as part of argparse when launching the program for the folder path.
        """
        self.aircraft_data = {'aircraft': pd.read_parquet('../data/aircraft.parquet')}
        self.aircraft_models_data = {'aircraft_models': pd.read_parquet('../data/aircraft_models.parquet')}
        self.airports_data = {'airports': pd.read_parquet('../data/airports.parquet')}
        self.carriers_data = {'carriers': pd.read_parquet('../data/carriers.parquet')}
        self.flights_data = {'flights': pd.read_parquet('../data/flights.parquet')}

        print('FlightData data loaded successfully...')

    def get_all_datasets(self) -> list[dict[str, pd.DataFrame]]:
        """
        Function called without arguments that iterates over all *_data instance attributes and returns them in a list.
        """
        return [self.aircraft_data, self.aircraft_models_data, self.airports_data, self.carriers_data, self.flights_data]

    def get_df_name(self, data: dict[str, pd.DataFrame]) -> str:
        """
        Function called with a single *_data instance attribute as argument. *_data instances contain a key, which is the name, and a pd.Dataframe.\
            The name is returned.
        """
        keys = list(data.keys())
        return keys[0]

    def get_df_columns(self, df: pd.DataFrame) -> list[str]:
        """
        Function called with a pd.DataFrame that returns a list[str] of all its columns
        """
        return list(df.columns)

    def count_df_rows(self, df: pd.DataFrame) -> int:
        """
        Function called with a pd.DataFrame that returns the count of its rows as int.
        """
        return len(df.index)

    def get_active_aircraft(self) -> pd.DataFrame:
        """
        Function that queries the pd.DataFrame stored in self.aircraft_data for all aircraft that are currently active,\
            indicated by status_code == 'A'.

        A new pd.DataFrame is returned with the results filtered containing only aircraft that are active.
        """
        return self.aircraft_data['aircraft'].query('status_code == "A"', inplace=False)

    def get_filter_query(self, filter_by: dict[str, str | None]) -> str:
        """
        Function designed to convert a dict of str,str pairs into a query string that is usable with the pd.DataFrame query function.\
            None values are cleared and their keys removed using self.clear_filter_by. An empty string is returned if no keys with not-None values were found.

        Example of how the string would be used:

        example_dataframe.query(query_string)
        """
        cleared_filter_by: dict[str, str] = self.clear_filter_by(filter_by)
        filters: list[str] = []

        for key, value in cleared_filter_by.items():
            filters.append('({0} == "{1}")'.format(key, value))

        filter_query = ' & '.join(filters)

        return filter_query

    def clear_filter_by(self, filter_by: dict[str, str | None]) -> dict[str, str]:
        """
        Function responsible for clearing None values and their keys from a dict. It returns either a cleared or an empty dict.
        """
        cleared_filter_by: dict[str, str] = {}

        for key, value in filter_by.items():
            if value is not None:
                cleared_filter_by[key] = value

        return cleared_filter_by

    def list_loaded_datasets(self) -> str:
        """
        Function intended to provide output for an API endpoint /datasets.

        It gathers all of the datasets loaded into the class and collects information about their pd.DataFrames.\
            The data collected is: Name of the pd.DataFrame, names of its columns in a list, and a total number of rows it contains.

        Gathered data is outputted as CSV in str form. 
        """
        datasets = self.get_all_datasets()
        dataset_specs: dict[str, list[Any]] = {'name': [], 'columns': [], 'rowcount': []}

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

    def list_aircraft_models(self) -> str:
        """
        Function intended to provide output for an API endpoint /aircraft/models.

        pd.DataFrame aircraft is accessed and queried for the model, manufacturer, and seats columns. That data is sorted by model, ascending.

        Gathered data is outputted as CSV in str form. 
        """
        df: pd.DataFrame = self.aircraft_models_data['aircraft_models']
        df.sort_values(by=['model'])

        return df.to_csv(columns=['model', 'manufacturer', 'seats'], header=True, index=False)

    # Needed for /active_aircraft endpoint
    def list_active_aircraft(self, filter_by: dict[str, str | None]) -> str:
        """
        Function intended to provide output for an API endpoint /aircraft/active where query strings manufacturer and model can be provided by the user.

        From the aircract pd.DataFrame, values are first filtered to only include active aircraft. The frame is then joined with the aircraft_models frame\
            on aircraft_model_code. That joined frame is then filtered as specified in the original query string.

        Gathered data is outputted as CSV in str form. If not filters are provided, all data is returned. If the filters match no data, only the CSV header is returned.
        """
        df_aircraft_models = self.aircraft_models_data['aircraft_models']
        df_aircraft = self.get_active_aircraft()

        df_joined = df_aircraft.set_index('aircraft_model_code').join(
            df_aircraft_models.set_index('aircraft_model_code'), rsuffix='_2')

        filter_query = self.get_filter_query(filter_by)
        if filter_query:
            df_joined.query(filter_query, inplace=True)

        return df_joined.to_csv(columns=['manufacturer', 'model', 'seats', 'aircraft_serial', 'name', 'county'], header=True, index=False)

    def count_active_aircraft(self) -> Any:
        """
        Currently not implemented. I will do it if I have time leftover after getting the first working version that can be submitted ready.
        """

        return NotImplemented
