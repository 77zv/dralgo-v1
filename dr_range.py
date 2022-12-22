import pandas as pd
from pandas import DataFrame


def bias(df: DataFrame) -> DataFrame:
    """
    It takes a dataframe as input, and returns the highest high and lowest low of the dataframe

    :param df: The dataframe containing the data
    :return: The highest high and lowest low of the dataframe
    """

    # Select only the rows between 9:30 and 10:30
    df_range: DataFrame = df.set_index('time').between_time('9:30', '10:30')

    # Taking the max and min of the dataframe for each day and renaming the columns.
    df_high: DataFrame = df_range.groupby(df_range.index.date).max().rename(
        columns={'mid_o': 'dr_high_o', 'mid_h': 'dr_high_h', 'mid_l': 'dr_high_l', 'mid_c': 'dr_high_c'})
    df_low: DataFrame = df_range.groupby(df_range.index.date).min().rename(
        columns={'mid_o': 'dr_low_o', 'mid_h': 'dr_low_h', 'mid_l': 'dr_low_l', 'mid_c': 'dr_low_c'})

    dr_range = pd.concat([df_low, df_high], axis=1)
    # adds column that is 50% of the high and low
    dr_range['dr_equilibrium'] = (dr_range['dr_high_h'] + dr_range['dr_low_l']) / 2

    dr_indicator = {}
    for date, row in dr_range.iterrows():
        dr_indicator[date] = {'dr_high_h': row['dr_high_h'], 'dr_low_l': row['dr_low_l'], 'dr_equilibrium': row['dr_equilibrium']}

    dr_indicator = pd.DataFrame.from_dict(dr_indicator).T

    return dr_indicator