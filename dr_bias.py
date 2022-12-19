import pandas
import pandas as pd
from pandas import DataFrame


def bias(df: DataFrame):
    """
    It takes a dataframe as input, and returns the highest high and lowest low of the dataframe

    :param df: The dataframe containing the data
    :return: The highest high and lowest low of the dataframe
    """

    # Select only the rows between 9:30 and 10:30


    df_range = df.set_index('time').between_time('9:30', '10:30').reset_index()

    print(df_range)
    # Find the highest high and lowest low
    highest_high = df_range['mid_h'].max()
    lowest_low = df_range['mid_l'].min()
    return highest_high, lowest_low



