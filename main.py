from oanda_api import OandaAPI
from dr_range import bias
import pandas as pd

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")
    print(SPX.df.tail())
    print(SPX.df.dtypes)

    pd.reset_option('max_columns')
    dr_low, dr_high, dr_range = bias(SPX.df)
    print(f"The Defining Range is defined by the following candles \n{dr_range.tail(13)}\n")
    print(f"The highs of the last 3 Defining Ranges \n{dr_high.tail(3)}\n")
    print(f"The lows of the last 3 Defining Ranges \n{dr_low.tail(3)}\n")

    # SPX.df = pd.concat([SPX.df, dr_range], axis=1)
    # print(f"Historic Data combined with the Defining Range: \n{SPX.df.tail(26)}\n")
