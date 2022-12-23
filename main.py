from pandas import DataFrame

from oanda_api import OandaAPI
from dr_range import create_dr_indicator
import pandas as pd

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")

    dr_indicator = create_dr_indicator(SPX.df)

    # loop through each row in the dataframe and add the dr_high_h and dr_low_l to the dataframe for that day
    def add_dr_indicator(indicator: DataFrame, df: DataFrame) -> DataFrame:
        for date, row in indicator.iterrows():
            for date2, row2 in df.iterrows():
                if date == date2.date():
                    SPX.df.loc[date2, 'dr_high_h'] = row['dr_high_h']
                    SPX.df.loc[date2, 'dr_low_l'] = row['dr_low_l']
                    SPX.df.loc[date2, 'dr_equilibrium'] = row['dr_equilibrium']
        return df
    add_dr_indicator(dr_indicator, SPX.df)
    print(SPX.df.tail(500))
