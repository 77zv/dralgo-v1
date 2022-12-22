from oanda_api import OandaAPI
from dr_range import bias
import pandas as pd

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")
    print(SPX.df.tail())
    print(SPX.df.dtypes)

    dr_indicator = bias(SPX.df)
    print(f"The Defining Range is defined by the following candles \n{dr_indicator}\n")

    # iterate through dr_range and adds the dr_high_h and dr_low_l to a dictionary with the key being the date

