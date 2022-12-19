from oanda_api import OandaAPI
from dr_bias import bias

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")
    print(SPX.df)
    print(SPX.df.dtypes)

    highest_high, lowest_low = bias(SPX.df)
    print(f"Highest high: {highest_high}")
    print(f"Lowest low: {lowest_low}")
