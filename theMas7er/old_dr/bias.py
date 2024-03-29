from typing import Tuple, Any

import pandas as pd
from datetime import datetime
from pandas import DataFrame


def evaluate_dr_bias(row) -> str | tuple[str, Any]:
    """
    If the close is greater than the daily range high, return 'Above DR High'. If the close is less than the daily range
    low, return 'Below DR Low'. Otherwise, return 'Between DR High and Low'

    :param row: the row of the dataframe that is being iterated over
    :return: A string
    """

    def evaluate_time(df_row) -> bool:
        """
        It takes a row of a dataframe as input, and returns True if the time of the row is greater than 10:30, and False
        otherwise

        :param df_row: the row of the dataframe that is being evaluated
        :return: A boolean value
        """
        return df_row.name.time() > datetime.strptime('10:30', '%H:%M').time()

    if row['mid_c'] > row['dr_high_h'] and evaluate_time(row):
        return 'bullish'
    elif row['mid_c'] < row['dr_low_l'] and evaluate_time(row):
        return 'bearish'


def evaluate_bias_time(row) -> str | tuple[str, Any]:
    """
    If the close is greater than the daily range high, return 'Above DR High'. If the close is less than the daily range
    low, return 'Below DR Low'. Otherwise, return 'Between DR High and Low'

    :param row: the row of the dataframe that is being iterated over
    :return: A string
    """

    def evaluate_time(df_row) -> bool:
        """
        It takes a row of a dataframe as input, and returns True if the time of the row is greater than 10:30, and False
        otherwise

        :param df_row: the row of the dataframe that is being evaluated
        :return: A boolean value
        """
        return df_row.name.time() > datetime.strptime('10:30', '%H:%M').time()

    if row['mid_c'] > row['dr_high_h'] and evaluate_time(row):
        return row.name.time()
    elif row['mid_c'] < row['dr_low_l'] and evaluate_time(row):
        return row.name.time()


def add_dr_bias(bias: DataFrame, df: pd.DataFrame) -> DataFrame:
    """
    For each date in the bias dataframe, find the corresponding date in the main dataframe and add the bias value to the
    main dataframe

    :param bias: DataFrame
    :param df: the dataframe to add the bias to
    :return: A dataframe with the bias added to it.
    """
    for date, row in bias.iterrows():
        for date2, row2 in df.iterrows():
            if date == date2.date():
                df.loc[date2, 'dr_bias'] = row['dr_bias']
                df.loc[date2, 'bias_time'] = row['bias_time']
    return df


def evaluate_daily_candle_close(row: DataFrame) -> str:
    """
    If the midpoint of the close price is greater than the midpoint of the open price, return 'bullish', else if the
    midpoint of the close price is less than the midpoint of the open price, return 'bearish', else return 'neutral'

    :param row: DataFrame - the row of data that we're evaluating
    :return: A string
    """
    if row['mid_c'] > row['mid_o']:
        return 'bullish'
    elif row['mid_c'] < row['mid_o']:
        return 'bearish'
    return 'neutral'


def test_bias(row: DataFrame) -> int:
    """
    If the daily candle bias is the same as the daily range bias, return 1, else return 0

    :param daily_df: DataFrame
    :return: 1 or 0
    """
    if row['daily_close'] == row['dr_bias']:
        return 1
    return 0
