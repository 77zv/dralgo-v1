import pandas as pd
from datetime import datetime

from pandas import DataFrame


def evaluate_dr_bias(row) -> str:
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


def add_bias(bias: DataFrame, df: pd.DataFrame) -> DataFrame:
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
    return df


def evaluate_daily_bias(daily_df: DataFrame):
    if daily_df['mid_c'] > daily_df['mid_o']:
        return 'bullish'
    elif daily_df['mid_c'] < daily_df['mid_o']:
        return 'bearish'


def test_bias(daily_df: DataFrame):
    if daily_df['daily_candle_bias'] == daily_df['dr_bias']:
        return 1
    return 0
