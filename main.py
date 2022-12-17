from oanda_api import OandaAPI

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")
    print(SPX.df)
    print(SPX.df.dtypes)
