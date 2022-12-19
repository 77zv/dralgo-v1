from oanda_api import OandaAPI
from dr_bias import bias

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")
    # print(SPX.df.tail(120))

    dr_highs, dr_lows, dr_range = bias(SPX.df)
    print(f"The Defining Range is defined by the following candles \n{dr_range.tail(13)}\n")
    print(f"The highs of the last 3 Defining Ranges \n{dr_highs.tail(3)}\n")
    print(f"The lows of the last 3 Defining Ranges \n{dr_lows.tail(3)}\n")
