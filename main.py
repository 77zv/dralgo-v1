import pandas as pd

from pandas import DataFrame
from oanda_api import OandaAPI

from theMas7er.dr_setup import backtesting_dr

pd.set_option('display.max_rows', 1000)

SPX: OandaAPI = OandaAPI()
data : DataFrame = SPX.create_data("SPX500_USD", "M15")
print(data)

backtesting_dr(data, "9:30", "10:30", 10000, 0.02)