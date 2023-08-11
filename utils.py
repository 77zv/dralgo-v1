import datetime
import calendar
import time
from enum import Enum


def his_data_filepath(pair, granularity):
    """
    It takes a pair and a granularity and returns a filepath

    :param pair: The currency pair to download data for
    :param granularity: The candlestick chart's time interval. Valid values are:
    :return: A list of dictionaries.
    """
    return f"his_data/{pair}_{granularity}.pkl"


# returns month start and end dates in Unix time
def get_months(num_months) -> tuple:
    today = time.time()
    current_year = time.localtime(today).tm_year
    current_month = time.localtime(today).tm_mon
    current_day = time.localtime(today).tm_mday
    current_hour = time.localtime(today).tm_hour
    current_minute = time.localtime(today).tm_min
    current_second = time.localtime(today).tm_sec

    start_dates = []
    end_dates = []

    for i in range(num_months):
        year = current_year
        month = current_month - i

        if month <= 0:
            year -= 1
            month = 12 + month

        last_day = calendar.monthrange(year, month)[1]
        last_day = min(last_day, current_day if month == current_month else last_day)

        first_date_unix = calendar.timegm((year, month, 1, 0, 0, 0))

        if month == current_month:
            end_date_unix = calendar.timegm((year, month, last_day, current_hour, current_minute, current_second))
        else:
            end_date_unix = calendar.timegm((year, month, last_day, 23, 59, 59))

        start_dates.append(first_date_unix)
        end_dates.append(end_date_unix)

    return start_dates, end_dates

# returns week start and end dates in Unix time
def get_weeks(num_weeks) -> tuple:
    today = time.time()
    current_year = time.localtime(today).tm_year
    current_month = time.localtime(today).tm_mon
    current_day = time.localtime(today).tm_mday
    current_hour = time.localtime(today).tm_hour
    current_minute = time.localtime(today).tm_min
    current_second = time.localtime(today).tm_sec

    start_dates = []
    end_dates = []

    for i in range(num_weeks):
        current_weekday = calendar.weekday(current_year, current_month, current_day)
        days_to_subtract = current_weekday + 7 * i

        year, month, day = current_year, current_month, current_day
        if days_to_subtract >= day:
            month -= 1
            if month <= 0:
                year -= 1
                month = 12 + month
            day = calendar.monthrange(year, month)[1] - (days_to_subtract - day)

        else:
            day -= days_to_subtract

        first_date_unix = calendar.timegm((year, month, day, 0, 0, 0))

        if current_weekday == 6 or i == 0:
            if i == 0:
                end_date_unix = calendar.timegm((current_year, current_month, current_day, current_hour, current_minute, current_second))
            else:
                days_to_add = 6 - current_weekday
                end_date_unix = calendar.timegm((year, month, day + days_to_add, 23, 59, 59))
        else:
            days_to_add = 6 - current_weekday
            end_date_unix = calendar.timegm((year, month, day + days_to_add, 23, 59, 59))

        start_dates.append(first_date_unix)
        end_dates.append(end_date_unix)

    return start_dates, end_dates

class Color(Enum):
    # Define ANSI color codes
    RED ="\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA_BG = "\u001b[45m"
    BLACK = "\u001b[40m"
    RESET = "\033[0m"  # Reset text attributes to default
