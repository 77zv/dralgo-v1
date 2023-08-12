import os
import time
from typing import Callable

import pandas as pd
import pytz

from pandas import DataFrame

from data.oanda_api import OandaAPI
from utils import get_weeks
from utils import Color


def backtesting_dr(df: DataFrame, range_start_time: str, range_end_time: str, initial_balance: float,
                   risk_percent: float, rr: int) -> float:
    balance = initial_balance
    trades = []

    for date, date_data in df.groupby(df.index.date):
        date_range_data = date_data.between_time(range_start_time, range_end_time, inclusive="left")

        print(f"Data for {date}:")
        print(date_range_data)

        # Calculate the highest high and lowest low within the specified time range
        if not date_range_data.empty:
            highest_high = date_range_data["mid_h"].max()
            lowest_low = date_range_data["mid_l"].min()

            print(Color.GREEN.value + f"Highest High in the specified time range: {highest_high}" + Color.RESET.value)
            print(Color.GREEN.value + f"Lowest Low in the specified time range: {lowest_low}" + Color.RESET.value)

            # Check if the price first closes above or below the range after the range end time and in the same day
            end_time = pd.Timestamp(date).replace(hour=int(range_end_time[:2]), minute=int(range_end_time[3:]),
                                                  second=0, microsecond=0)
            eastern_tz = pytz.timezone('US/Eastern')
            end_time = eastern_tz.localize(end_time)

            # The data after the range end time
            after_range_end = date_data[date_data.index >= end_time]

             if not after_range_end.empty:
                above_high_after_range = after_range_end[after_range_end["mid_c"] > highest_high]
                below_low_after_range = after_range_end[after_range_end["mid_c"] < lowest_low]

                # Check if the price first closes above or below the range after the range end time and in the same day
                if not below_low_after_range.empty and not above_high_after_range.empty and \
                        above_high_after_range.index[0] < below_low_after_range.index[0]:
                    below_low_after_range = DataFrame()
                elif not below_low_after_range.empty and not above_high_after_range.empty and \
                        below_low_after_range.index[0] < above_high_after_range.index[0]:
                    above_high_after_range = DataFrame()

                if not above_high_after_range.empty:
                    first_close_above_high_time = above_high_after_range.index[0]

                    print(
                        Color.YELLOW.value + f"First close above highest high after range end time at: {first_close_above_high_time}" + Color.RESET.value)

                    # Separate the data into two parts based on the closing condition
                    after_above_high = date_data[date_data.index > first_close_above_high_time]

                    # Check if price trades into 50% of the range after closing above the range
                    fifty_percent_level = ((highest_high - lowest_low) / 2.0) + lowest_low
                    trade_into_range = False  # Initialize the variable
                    trade_into_50_percent_time = None  # Initialize the variable to store the time

                    for _, row in after_above_high.iterrows():
                        if row["mid_l"] < fifty_percent_level:
                            trade_into_range = True
                            trade_into_50_percent_time = row.name
                            break

                    if trade_into_range:

                        after_trade_into_50_percent = date_data[date_data.index > trade_into_50_percent_time]

                        # Check if price hits stop loss or take profit first
                        take_profit = fifty_percent_level + ((highest_high - fifty_percent_level) * rr)
                        stop_loss = lowest_low

                        print(
                            Color.BLUE.value + f"Price trades into 50% of the range after closing above the range at: {trade_into_50_percent_time}. Price: {row['mid_c']}, Stop Loss: {stop_loss}, Take Profit: {take_profit}" + Color.RESET.value)

                        trade_closed = False  # Initialize the variable to track if the trade is closed

                        for _, row in after_trade_into_50_percent.iterrows():
                            if row["mid_h"] >= take_profit:
                                balance += balance * risk_percent
                                print(
                                    Color.BLUE.value + f"Take profit hit at: {row.name}. New balance: {balance}" + Color.RESET.value)
                                trades.append({
                                    "Time": row.name,
                                    "Trade Type": "Take Profit",
                                    "Price": row["mid_h"],
                                    "Balance Change": balance * risk_percent
                                })
                                trade_closed = True
                                break
                            elif row["mid_l"] <= stop_loss:
                                balance -= balance * risk_percent
                                print(
                                    Color.RED.value + f"Stop loss hit at: {row.name}. New balance: {balance}" + Color.RESET.value)
                                trades.append({
                                    "Time": row.name,
                                    "Trade Type": "Stop Loss",
                                    "Price": row["mid_l"],
                                    "Balance Change": -balance * risk_percent
                                })
                                trade_closed = True
                                break

                        # if the trade is not closed by 16:45, close it automatically
                        if not trade_closed and after_trade_into_50_percent.index[-1].time() >= pd.Timestamp(
                                "16:45").time():

                            if row["mid_c"] >= fifty_percent_level:
                                above_fifty_percent_level_after_close = (row["mid_c"] - fifty_percent_level) / (
                                        take_profit - fifty_percent_level) * risk_percent * balance
                                balance += above_fifty_percent_level_after_close
                                print(
                                    Color.RED.value + f"Trade automatically closed at {after_trade_into_50_percent.index[-1]}. New balance: {balance}, taking a win of +{above_fifty_percent_level_after_close}" + Color.RESET.value)
                                trades.append({
                                    "Time": after_trade_into_50_percent.index[-1],
                                    "Trade Type": "Auto Close - Win",
                                    "Price": row["mid_c"],
                                    "Balance Change": above_fifty_percent_level_after_close
                                })
                            else:
                                below_fifty_percent_level_after_close = (fifty_percent_level - row["mid_c"]) / (
                                        fifty_percent_level - take_profit) * risk_percent * balance
                                balance -= below_fifty_percent_level_after_close
                                print(
                                    Color.RED.value + f"Trade automatically closed at {after_trade_into_50_percent.index[-1]}. New balance: {balance}, taking a loss of -{below_fifty_percent_level_after_close}" + Color.RESET.value)
                                trades.append({
                                    "Time": after_trade_into_50_percent.index[-1],
                                    "Trade Type": "Auto Close - Loss",
                                    "Price": row["mid_c"],
                                    "Balance Change": -below_fifty_percent_level_after_close
                                })

                    else:
                        print(
                            Color.RED.value + "Price did not trade into 50% of the range after closing above the range." + Color.RESET.value)

                if not below_low_after_range.empty:
                    first_close_below_low_time = below_low_after_range.index[0]
                    print(
                        Color.YELLOW.value + f"First close below lowest low after range end time at: {first_close_below_low_time}" + Color.RESET.value)

                    # Separate the data into two parts based on the closing condition
                    after_below_low = date_data[date_data.index > first_close_below_low_time]

                    # Check if price trades into 50% of the range after closing below the range
                    fifty_percent_level = ((highest_high - lowest_low) / 2.0) + lowest_low
                    trade_into_range = False  # Initialize the variable
                    trade_into_50_percent_time = None  # Initialize the variable to store the time

                    for _, row in after_below_low.iterrows():
                        if row["mid_h"] > fifty_percent_level:
                            trade_into_range = True
                            trade_into_50_percent_time = row.name
                            break

                    if trade_into_range:

                        after_trade_into_50_percent = date_data[date_data.index > trade_into_50_percent_time]

                        # Check if price hits stop loss or take profit first
                        take_profit = fifty_percent_level - ((fifty_percent_level - lowest_low) * rr)
                        stop_loss = highest_high

                        print(
                            Color.BLUE.value + f"Price trades into 50% of the range after closing below the range at: {trade_into_50_percent_time}. Price: {row['mid_c']}, Stop Loss: {stop_loss}, Take Profit: {take_profit}" + Color.RESET.value)
                        trade_closed = False  # Initialize the variable to track if the trade is closed

                        for _, row in after_trade_into_50_percent.iterrows():
                            if row["mid_l"] <= take_profit:
                                balance += balance * risk_percent
                                print(
                                    Color.BLUE.value + f"Take profit hit at: {row.name}. New balance: {balance}" + Color.RESET.value)
                                trades.append({
                                    "Time": row.name,
                                    "Trade Type": "Take Profit",
                                    "Price": row["mid_l"],
                                    "Balance Change": balance * risk_percent
                                })
                                trade_closed = True
                                break
                            elif row["mid_h"] >= stop_loss:
                                balance -= balance * risk_percent
                                print(
                                    Color.RED.value + f"Stop loss hit at: {row.name}. New balance: {balance}" + Color.RESET.value)
                                trades.append({
                                    "Time": row.name,
                                    "Trade Type": "Stop Loss",
                                    "Price": row["mid_h"],
                                    "Balance Change": -balance * risk_percent
                                })
                                trade_closed = True
                                break

                        # if the trade is not closed by 16:45, close it automatically
                        if not trade_closed and after_trade_into_50_percent.index[-1].time() >= pd.Timestamp(
                                "16:45").time():

                            if row["mid_c"] >= fifty_percent_level:
                                above_fifty_percent_level_after_close = (row["mid_c"] - fifty_percent_level) / (
                                        take_profit - fifty_percent_level) * risk_percent * balance
                                balance -= above_fifty_percent_level_after_close
                                print(
                                    Color.RED.value + f"Trade automatically closed at {after_trade_into_50_percent.index[-1]}. New balance: {balance}, taking a loss of -{above_fifty_percent_level_after_close}" + Color.RESET.value)
                                trades.append({
                                    "Time": after_trade_into_50_percent.index[-1],
                                    "Trade Type": "Auto Close - Loss",
                                    "Price": row["mid_c"],
                                    "Balance Change": -above_fifty_percent_level_after_close
                                })
                            else:
                                below_fifty_percent_level_after_close = (fifty_percent_level - row["mid_c"]) / (
                                        fifty_percent_level - take_profit) * risk_percent * balance
                                balance += below_fifty_percent_level_after_close
                                print(
                                    Color.RED.value + f"Trade automatically closed at {after_trade_into_50_percent.index[-1]}. New balance: {balance}, taking a win of +{below_fifty_percent_level_after_close}" + Color.RESET.value)
                                trades.append({
                                    "Time": after_trade_into_50_percent.index[-1],
                                    "Trade Type": "Auto Close - Win",
                                    "Price": row["mid_c"],
                                    "Balance Change": below_fifty_percent_level_after_close
                                })

                    else:
                        print(
                            Color.RED.value + "Price did not trade into 50% of the range after closing below the range." + Color.RESET.value)

        print("\n")
    print(Color.BLUE.value + f"Final balance: {balance}" + Color.RESET.value)

    # Write trades to CSV
    trades_df = pd.DataFrame(trades)

    # Append new trades to existing CSV file if it exists, otherwise create a new file
    try:
        existing_trades_df = pd.read_csv("trades.csv")
        combined_trades_df = pd.concat([existing_trades_df, trades_df], ignore_index=True)
        combined_trades_df.to_csv("trades.csv", index=False)
    except FileNotFoundError:
        trades_df.to_csv("trades.csv", index=False)

    return balance


def run_backtest(callback: Callable, initial_balance: float, risk: float, rr: int, num_weeks: int):
    pd.set_option('display.max_rows', 1000)
    # Create a fresh new CSV file for trades
    trades_filename = "trades.csv"
    if os.path.exists(trades_filename):
        os.remove(trades_filename)

    spx: OandaAPI = OandaAPI()

    # start_dates, end_dates = get_months(num_months)
    start_dates, end_dates = get_weeks(num_weeks)

    balance = initial_balance

    for i in range(num_weeks):
        start_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_dates[i]))
        end_date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_dates[i]))
        print(f"Week {i + 1}: Start Date: {start_date_str}, End Date: {end_date_str}")

        data: DataFrame = spx.create_data("SPX500_USD", "M15", 4000, start_dates[i], end_dates[i])
        balance: float = backtesting_dr(data, "9:30", "10:30", balance, risk, rr)

    print(
        Color.BLACK.value + f"Initial Balance: {initial_balance}, Risk: {risk * 100}%, RR: {rr} \nFinal Balance: {balance} with a return of {((balance - initial_balance) / initial_balance) * 100}%" + Color.RESET.value)
