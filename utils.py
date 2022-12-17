def his_data_filepath(pair, granularity):
    """
    It takes a pair and a granularity and returns a filepath

    :param pair: The currency pair to download data for
    :param granularity: The candlestick chart's time interval. Valid values are:
    :return: A list of dictionaries.
    """
    return f"his_data/{pair}_{granularity}.pkl"