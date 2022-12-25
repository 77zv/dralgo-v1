from oanda_api import OandaAPI
from dr_range import *
from bias import *

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5")

    # only keep candles after 9:30 before 16:00
    trading_day: DataFrame = SPX.df.between_time('9:30', '16:00').copy()

    # Creating a dataframe with the defining range of the SPX500.
    dr_indicator: DataFrame = create_dr_indicator(trading_day)

    # Adding the defining range indicator to the trading day dataframe.
    dr_df: DataFrame = add_dr_indicator(dr_indicator, trading_day)

    # Applying the function evaluate_dr_bias to each row of the dataframe.
    dr_df['dr_bias'] = dr_df.apply(evaluate_dr_bias, axis=1)

    # Grouping the dataframe by date and then taking the first value of the column 'dr_position'.
    dr_bias: DataFrame = pd.DataFrame(dr_df.groupby(dr_df.index.date)['dr_bias'].first())

    # Creating a new dataframe that only contains the data we need for a trade
    simulation_data: DataFrame = dr_df.between_time('10:30', '16:00')[['mid_o', 'mid_h', 'mid_l', 'mid_c', 'dr_bias', 'dr_equilibrium']].copy()

    # Adding the bias to the trading times dataframe.
    dr_trades = add_bias(dr_bias, simulation_data)

    print(dr_trades.tail(50))
