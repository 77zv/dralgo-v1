import pandas as pd
from datetime import datetime


def evaluate_dr_bias(row):
    """
    If the close is greater than the daily range high, return 'Above DR High'. If the close is less than the daily range
    low, return 'Below DR Low'. Otherwise, return 'Between DR High and Low'

    :param row: the row of the dataframe that is being iterated over
    :return: A string
    """
    if row['mid_c'] > row['dr_high_h'] and row.name.time() > datetime.strptime('10:30', '%H:%M').time():
        return 'Above DR High'
    elif row['mid_c'] < row['dr_low_l'] and row.name.time() > datetime.strptime('10:30', '%H:%M').time():
        return 'Below DR Low'
