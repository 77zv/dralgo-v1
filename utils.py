import datetime

def his_data_filepath(pair, granularity):
    """
    It takes a pair and a granularity and returns a filepath

    :param pair: The currency pair to download data for
    :param granularity: The candlestick chart's time interval. Valid values are:
    :return: A list of dictionaries.
    """
    return f"his_data/{pair}_{granularity}.pkl"


# returns week start dates in Unix time
def get_dates_in_unix_time_past(num_w):
    # Get the current date and time
    today = datetime.datetime.now()

    # Find the last Monday
    current_day_of_week = today.weekday()
    days_until_last_monday = (current_day_of_week + 1) % 7
    start_date = today - datetime.timedelta(days=days_until_last_monday)

    dates_unix_time = []
    for week in range(num_w):
        # Generate dates for Monday and Friday in each week
        monday_date = start_date - datetime.timedelta(weeks=week)
        friday_date = start_date - datetime.timedelta(weeks=week, days=4)

        # Convert dates to Unix time
        monday_unix_time = int(monday_date.timestamp())
        friday_unix_time = int(friday_date.timestamp())

        # Append the Monday and Friday dates to the 2D array
        dates_unix_time.append([datetime.datetime.fromtimestamp(monday_unix_time).isoformat(), datetime.datetime.fromtimestamp(friday_unix_time).isoformat()])

    return dates_unix_time
