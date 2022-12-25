from oanda_api import OandaAPI
from bias import *
from dr_trade_simulation import *

if __name__ == "__main__":
    exec(open('dr_trade_simulation.py').read())
    daily = OandaAPI()
    daily.create_data("SPX500_USD", "D")

    daily_df = daily.df.copy()

    daily_df = add_bias(dr_bias, daily_df)
    print(daily_df.tail(50))

