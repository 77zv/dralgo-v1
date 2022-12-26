from oanda_api import OandaAPI
from dr_range import *
from bias import *
import time

if __name__ == "__main__":
    SPX = OandaAPI()
    SPX.create_data("SPX500_USD", "M5", 5000)

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
    simulation_data: DataFrame = dr_df.between_time('10:30', '16:00')[
        ['mid_o', 'mid_h', 'mid_l', 'mid_c', 'dr_bias', 'dr_low_l', 'dr_high_h', 'dr_equilibrium']].copy()

    # Adding the bias to the trading times dataframe.
    dr_trades = add_dr_bias(dr_bias, simulation_data)
    dr_trades.dropna(inplace=True)

    print(dr_trades)

    # Initialize variables to track the current position and account balance
    position = 0  # 0 for no position, 1 for long position, -1 for short position
    balance = 10000  # Initial account balance

    # Iterate over the rows of the dr_trades dataframe
    for index, row in dr_trades.iterrows():
        # Get the current time
        current_time = time.strftime("%H:%M", time.localtime())

        # Check if the current time is 4:00 PM ET
        if current_time == '16:00':
            # Close any open positions
            if position == 1:
                # We have a long position. Sell at the current price and update the balance and position
                balance += row['mid_c'] - row['dr_equilibrium']
                position = 0
            elif position == -1:
                # We have a short position. Buy at the current price and update the balance and position
                balance += row['dr_equilibrium'] - row['mid_c']
                position = 0


        # Check if we have a long or short position
        else:
            if position == 1:
                # We have a long position. Check if the price has hit the take profit level
                if row['mid_h'] >= row['dr_high_h']:
                    # Sell at the take profit level and update the balance and position
                    balance += row['dr_high_h'] - row['dr_equilibrium']
                    position = 0
                # Check if the price has hit the stop loss level
                elif row['mid_h'] <= row['dr_low_l']:
                    # Sell at the stop loss level and update the balance and position
                    balance += row['dr_low_l'] - row['dr_equilibrium']
                    position = 0
            elif position == -1:
                # We have a short position. Check if the price has hit the take profit level
                if row['mid_l'] <= row['dr_low_l']:
                    # Buy at the take profit level and update the balance and position
                    balance += row['dr_equilibrium'] - row['dr_low_l']
                    position = 0
                # Check if the price has hit the stop loss level
                elif row['mid_l'] >= row['dr_high_h']:
                    # Buy at the stop loss level and update the balance and position
                    balance += row['dr_equilibrium'] - row['dr_high_h']
                    position = 0
            else:
                # We don't have a position. Check if the price has hit the equilibrium level
                if row['mid_h'] >= row['dr_equilibrium'] or row['mid_l'] <= row['dr_equilibrium']:
                    # Buy in the direction of the bias and update the position
                    position = 1 if row['dr_bias'] == 'Bullish' else -1

        # Print the final balance
    print(f'Initial balance: 10000 \nFinal balance: {balance} \nNet profit: {balance - 10000}')

