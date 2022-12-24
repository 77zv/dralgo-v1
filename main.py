from oanda_api import OandaAPI
from dr_range import *
from bias import evaluate_dr_bias

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")

    # only keep candles after 9:30 before 16:00
    SPX.df = SPX.df.between_time('9:30', '16:00')

    dr_indicator = create_dr_indicator(SPX.df)

    SPX.df = add_dr_indicator(dr_indicator, SPX.df)
    print(SPX.df.index.time)
    #
    SPX.df['dr_position'] = SPX.df.apply(evaluate_dr_bias, axis=1)
    dr_bias = SPX.df.groupby(SPX.df.index.date)['dr_position'].first()

    print(dr_bias)
