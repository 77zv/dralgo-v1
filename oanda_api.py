import requests
import pandas as pd
from pandas import DataFrame
from requests import Response

import defs


class OandaAPI:
    def __init__(self):
        self.session = requests.Session()

    def fetch_candles(self, pair_name: str, count: int, granularity: str) -> (int, Response):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        params: dict = dict(
            count=count,
            granularity=granularity,
            price="MBA"
        )
        response: Response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()

    @staticmethod
    def load_candles_data(json_response) -> DataFrame:
        """
        It takes a JSON response from the OANDA API and returns a Pandas DataFrame with the data in a format that's easier
        to work with

        :param json_response: The JSON response from the API
        :return: A dataframe with the following columns:
        """
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']
        our_data = []

        # loops through each candle in the 'candles' field of json_response
        for candle in json_response['candles']:
            if not candle['complete']:
                continue

            # creating a new dict and adding the 'time' and 'volume' from the response
            new_dict = {'time': candle['time'], 'volume': candle['volume']}

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

    def create_data(self, pair: str, granularity: str) -> None:
        """
        > It fetches 4000 candles from the Oanda API, loads the data into a Pandas DataFrame, prints the number of candles
        and the time range, and then saves the data to a PKL file

        :param pair: The currency pair to fetch data for
        :param granularity: The granularity of the candles to fetch. Valid values are:
        """
        response_code, json_data = self.fetch_candles(pair, 4000, granularity)
        if response_code != 200:
            print(f"Error: {response_code}")
            return
        df = self.load_candles_data(json_data)
        print(f"{pair} loaded {df.shape[0]} candles from {df.time.min()} to {df.time.max()}")
        self.save_file(df, pair, granularity)


if __name__ == "__main__":
    api = OandaAPI()
    api.create_data("SPX500_USD", "H1")
