import pandas as pd

from utils import get_dates_in_unix_time_past
from pandas import DataFrame
from oanda_api import OandaAPI

pd.set_option('display.max_rows', 1000)

num_weeks =4
dates = get_dates_in_unix_time_past(num_weeks)
print(dates)

SPX: OandaAPI = OandaAPI()
start_time = dates[len(dates) - 1][1]
end_time = dates[len(dates) - 1][0]
data : DataFrame = SPX.create_data("SPX500_USD", "D", 4000, start_time, end_time)
print(data)