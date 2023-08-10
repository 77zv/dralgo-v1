import array
from typing import Callable

import pandas as pd

from pandas import DataFrame
from oanda_api import OandaAPI
from utils import get_months, get_weeks
import time

from theMas7er.dr_setup import backtesting_dr

# num_months = 12
# start_dates, end_dates = get_months(num_months)
# for i in range(num_months):
#     start_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_dates[i]))
#     end_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_dates[i]))
#     print(f"Month {i + 1}: Start Date: {start_date_str}, End Date: {end_date_str}")

MAGENTA_BG = "\u001b[45m"
BLACK = "\u001b[40m"

def run_backtest(callback: Callable, initial_balance: float, risk : float, rr: int, num_months: int):
    pd.set_option('display.max_rows', 1000)

    spx: OandaAPI = OandaAPI()

    # start_dates, end_dates = get_months(num_months)
    start_dates, end_dates = get_weeks(num_months)

    balance = initial_balance

    for i in range(num_months):

        start_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_dates[i]))
        end_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_dates[i]))
        print(f"Month {i + 1}: Start Date: {start_date_str}, End Date: {end_date_str}")

        data: DataFrame = spx.create_data("SPX500_USD", "M15", 4000, start_dates[i], end_dates[i])
        balance: float = backtesting_dr(data, "9:30", "10:30", balance, risk, rr)

    print(BLACK + f"Initial Balance: {initial_balance}, Risk: {risk*100}%, RR: {rr} \nFinal Balance: {balance} with a return of {((balance - initial_balance) / initial_balance) * 100}%")


num_months = 12
run_backtest(backtesting_dr, 10000, 0.02, 1, 4)

# num_weeks = 52  # Replace with the number of weeks you want
# start_dates, end_dates = get_weeks(num_weeks)
# for i in range(num_weeks):
#     print(f"Week {i+1} - Start: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_dates[i]))}, End: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_dates[i]))}")


# start_dates, end_dates = get_months(12)
# for i in range(12):
#     start_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_dates[i]))
#     end_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_dates[i]))
#     print(f"Month {i + 1}: Start Date: {start_date_str}, End Date: {end_date_str}")
