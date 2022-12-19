from typing import Tuple

import pandas
import pandas as pd
from pandas import DataFrame


def bias(df: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
    It takes a dataframe as input, and returns the highest high and lowest low of the dataframe

    :param df: The dataframe containing the data
    :return: The highest high and lowest low of the dataframe
    """

    # Select only the rows between 9:30 and 10:30
    df_range: DataFrame = df.set_index('time').between_time('9:30', '10:30')

    # Grouping the dataframe by business day and then taking the max and min of each group.
    df_high: DataFrame = df_range.groupby(pd.Grouper(freq='B')).max().rename(
        columns={'mid_o': 'dr_high_o', 'mid_h': 'dr_high_h', 'mid_l': 'dr_high_l', 'mid_c': 'dr_high_c'})

    df_low: DataFrame = df_range.groupby(pd.Grouper(freq='B')).min().rename(
        columns={'mid_o': 'dr_low_o', 'mid_h': 'dr_low_h', 'mid_l': 'dr_low_l', 'mid_c': 'dr_low_c'})



    return df_high, df_low, df_range
