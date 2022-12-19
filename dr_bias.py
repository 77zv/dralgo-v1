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
    df_high: DataFrame = df_range.groupby(pd.Grouper(freq='B')).max()
    df_low: DataFrame = df_range.groupby(pd.Grouper(freq='B')).min()

    return df_high, df_low, df_range

