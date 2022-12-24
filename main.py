from oanda_api import OandaAPI
from dr_range import *
from bias import evaluate_dr_bias

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")

    # only keep candles after 9:30 before 16:00
    trading_day = SPX.df.between_time('9:30', '16:00').copy()

    # Creating a dataframe with the defining range of the SPX500.
    dr_indicator = create_dr_indicator(trading_day)

    dr_df = add_dr_indicator(dr_indicator, trading_day)

    dr_df['dr_position'] = dr_df.apply(evaluate_dr_bias, axis=1)
    dr_bias = dr_df.groupby(dr_df.index.date)['dr_position'].first()

    print(dr_bias)
