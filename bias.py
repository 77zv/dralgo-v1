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
        return 'Above DR High'
    elif row['mid_c'] < row['dr_low_l'] and evaluate_time(row):
        return 'Below DR Low'


def add_bias(bias: DataFrame, df: pd.DataFrame) -> DataFrame:
    for date, row in bias.iterrows():
        for date2, row2 in df.iterrows():
            if date == date2.date():
                df.loc[date2, 'dr_bias'] = row['dr_bias']
    return df

