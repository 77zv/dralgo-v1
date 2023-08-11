import time

import pytz
import requests
import pandas as pd
from pandas import DataFrame
from requests import Response

import defs


class OandaAPI:
    def __init__(self):
        self.df = None
        self.session = requests.Session()

    def fetch_candles(self, pair_name: str, granularity: str, count: int = 4000) -> (int, Response):
        """
        `fetch_candles` fetches the last `count` candles of `pair_name` with `granularity` and returns a tuple of the number
        of candles fetched and the response

        :param pair_name: The name of the pair you want to fetch candles for
        :param count: The number of candles to fetch
        :param granularity: The time interval between each candle. Valid values are:
        """
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        params: dict = dict(
            count=count,
            granularity=granularity,
            price="MBA",
        )
        response: Response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()

    def fetch_candles_from_dates(self, pair_name: str, granularity: str, start_time: int, end_time: int) -> (int, Response):
        """
        `fetch_candles` fetches the last `count` candles of `pair_name` with `granularity` and returns a tuple of the number
        of candles fetched and the response

        :param start_time: Start date range of candles
        :param end_time:  End date of range of candles
        :param pair_name: The name of the pair you want to fetch candles for
        :param granularity: The time interval between each candle. Valid values are:
        """
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        # params = {
        #     "granularity": granularity,
        #     "from": start_time,
        #     "to" : end_time,
        # }
        params = dict(
            granularity=granularity,
            price="MBA",
            from_=start_time,
            to=end_time,
        )
        response: Response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        print(f"url: {response.url}")
        # print the url for debugging
        return response.status_code, response.json()


    @staticmethod
    def load_candles_data(json_response) -> DataFrame:
        """
        It takes a JSON response from the OANDA API and returns a Pandas DataFrame with the data in a format that's easier
        to work with

        :param json_response: The JSON response from the API
        :return: A dataframe with the following columns:
        """
        ohlc = ['o', 'h', 'l', 'c']
        our_data = []

        # loops through each candle in the 'candles' field of json_response
        for candle in json_response['candles']:
            if not candle['complete']:
                continue

            # creating a new dict and adding the 'time' and 'volume' from the response
            new_dict = {'time': candle['time']}

            # adding the 'ohlc' data to the dictionary
            for oh in ohlc:
                new_dict[f"{'mid'}_{oh}"] = candle['mid'][oh]

            our_data.append(new_dict)

        return pd.DataFrame.from_dict(our_data)

    @staticmethod
    def save_file(candles_df: DataFrame, pair: str, granularity: str):
        """
        > Save the dataframe to a pickle file

        :param candles_df: The dataframe of candles that we want to save
        :param pair: The currency pair you want to download
        :param granularity: The candlestick chart's time interval.
        """
        candles_df.to_pickle(f"his_data/{pair}_{granularity}.pkl")

    def create_data(self, pair: str, granularity: str, count: int = 4000, start_time: int  | None = None, end_time: int | None = None) -> DataFrame | None:
        """
        > It fetches 4000 candles from the Oanda API, loads the data into a Pandas DataFrame, prints the number of candles
        and the time range, and then saves the data to a PKL file

        :param end_time:
        :param start_time:
        :param count:
        :param pair: The currency pair to fetch data for
        :param granularity: The granularity of the candles to fetch. Valid values are:
        """

        if start_time is not None and end_time is not None:

            start_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time))
            end_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_time))

            print(f"Fetching candles from {start_date_str} to {end_date_str}")
            response_code, json_data = self.fetch_candles_from_dates(pair, granularity, start_time, end_time)
        else:
            response_code, json_data = self.fetch_candles(pair, granularity, count)

        if response_code != 200:
            print(f"Error: {response_code}")
            return

        self.df: DataFrame = self.load_candles_data(json_data)

        # converting the 'mod_col' from strings to floats
        mod_cols = ['mid_o', 'mid_h', 'mid_l', 'mid_c']
        self.df[mod_cols] = self.df[mod_cols].apply(pd.to_numeric)

        # Convert the time column to datetime objects
        self.df['time'] = pd.to_datetime(self.df['time'])
        # First, create a timezone object for Eastern Time
        et = pytz.timezone('US/Eastern')

        # Convert the time column to Eastern Time
        self.df['time'] = self.df['time'].dt.tz_convert(et)

        # Set the time column as the index
        self.df.set_index('time', inplace=True)

        print(f"{pair} loaded {self.df.shape[0]} candles from {self.df.index.min()} to {self.df.index.max()}")

        # remove every day of the week that is sunday
        self.df = self.df[self.df.index.dayofweek != 6]

        # save the dataframe to file
        self.save_file(self.df, pair, granularity)
        return self.df
