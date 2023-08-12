from pandas import DataFrame
import pandas as pd

from data.oanda_api import OandaAPI
from theMas7er.dr_setup import run_backtest, backtesting_dr
from utils import get_weeks
from ict.casper_smc_silver_bullet import fair_value_gap_strategy

weeks = 100
run_backtest(backtesting_dr, 10000, 0.02, 1, weeks)

pd.set_option('display.max_rows', 1000)
#
# spx: OandaAPI = OandaAPI()
#
# start_dates, end_dates = get_weeks(1)
# data: DataFrame = spx.create_data("SPX500_USD", "M15", 4000, start_dates[0], end_dates[0])
#
# fair_value_gap_strategy(data)