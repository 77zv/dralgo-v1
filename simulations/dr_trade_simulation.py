from data.oanda_api import OandaAPI
from theMas7er.old_dr.dr_range import *
from theMas7er.old_dr.bias import *
import pandas as pd

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
    dr_df['bias_time'] = dr_df.apply(evaluate_bias_time, axis=1)

    # Grouping the dataframe by date and then taking the first value of the column 'dr_position' and 'bias_time'.
    dr_bias: DataFrame = pd.DataFrame(dr_df.groupby(dr_df.index.date)[['dr_bias', 'bias_time']].first())

    # Creating a new dataframe that only contains the data we need for a trade
    simulation_data: DataFrame = dr_df.between_time('10:30', '16:00')[
        ['mid_o', 'mid_h', 'mid_l', 'mid_c', 'dr_bias', 'bias_time', 'dr_low_l', 'dr_high_h', 'dr_equilibrium']].copy()

    # Adding the bias to the trading times dataframe.
    dr_trades = add_dr_bias(dr_bias, simulation_data)
    dr_trades.dropna(inplace=True)

    # Initialize variables to track the current position and account balance
    position = 0  # 0 for no position, 1 for long position, -1 for short position
    balance = 10000  # Initial account balance
    last_trade_date = '0000-00-00'  # date the last trade was taken

    # Iterate over the rows of the dr_trades dataframe
    for index, row in dr_trades.iterrows():
        # Get the current time
        current_time = index.strftime("%H:%M")
        current_date = index.strftime("%Y-%m-%d")

        # Check if the current time is 4:00 PM ET
        if current_time == '16:00':
            # Close any open positions
            if position == 1:
                # We have a long position. Sell at the current price and update the balance and position
                balance += row['mid_c'] - row['dr_equilibrium']
                print(f"Closing at Market Close on {row.name}: long {row['mid_c'] - row['dr_equilibrium']}")
                position = 0
            elif position == -1:
                # We have a short position. Buy at the current price and update the balance and position
                balance += row['dr_equilibrium'] - row['mid_c']
                print(f"Closing at Market Close on {row.name}: short {row['dr_equilibrium'] - row['mid_c']}")

                position = 0

        # Check if we have a long or short position
        else:
            if position == 1:
                # We have a long position. Check if the price has hit the take profit level
                if row['mid_h'] >= row['dr_high_h']:
                    # Sell at the take profit level and update the balance and position
                    balance += (row['dr_high_h'] - row['dr_equilibrium'])
                    position = 0
                    print(f"Took a win on {row.name}: long +{row['dr_high_h'] - row['dr_equilibrium']}")
                # Check if the price has hit the stop loss level
                elif row['mid_h'] <= row['dr_low_l']:
                    # Sell at the stop loss level and update the balance and position
                    balance -= (row['dr_equilibrium'] - row['dr_low_l'])
                    position = 0
                    print(f"Took a loss on {row.name}: long {row['dr_low_l'] - row['dr_equilibrium']}")
            elif position == -1:
                # We have a short position. Check if the price has hit the take profit level
                if row['mid_l'] <= row['dr_low_l']:
                    # Buy at the take profit level and update the balance and position
                    balance += (row['dr_equilibrium'] - row['dr_low_l'])
                    position = 0
                    print(f"Took a win on {row.name}: short +{row['dr_equilibrium'] - row['dr_low_l']}")
                # Check if the price has hit the stop loss level
                elif row['mid_l'] >= row['dr_high_h']:
                    # Buy at the stop loss level and update the balance and position
                    balance -= (row['dr_high_h'] - row['dr_equilibrium'])
                    position = 0
                    print(f"Took a loss {row.name}: short {row['dr_equilibrium'] - row['dr_high_h']}")
            else:
                # We don't have a position. Check if the price has hit the equilibrium level
                if (row['mid_h'] >= row['dr_equilibrium'] and row['dr_bias'] == 'bearish') and index.strftime(
                        '%Y-%m-%d') != last_trade_date and index.strftime('%H:%M') > row.bias_time.strftime('%H:%M'):
                    # Buy in the direction of the bias and update the position
                    last_trade_date = index.strftime('%Y-%m-%d')
                    position = -1

                elif (row['mid_l'] <= row['dr_equilibrium'] and row['dr_bias'] == 'bullish') and index.strftime(
                        '%Y-%m-%d') != last_trade_date and index.strftime('%H:%M') > row.bias_time.strftime('%H:%M'):
                    last_trade_date = index.strftime('%Y-%m-%d')
                    position = 1

        # Print the final balance
    print(f'Initial balance: 10000 \nFinal balance: {balance} \nNet profit: {balance - 10000}')
