import pandas as pd
import pytz

from pandas import DataFrame
from oanda_api import OandaAPI

pd.set_option('display.max_rows', 1000)

# Define ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"  # Reset text attributes to default


def backtesting_dr(df: DataFrame, range_start_time: str, range_end_time: str):
    for date, date_data in df.groupby(df.index.date):
        date_range_data = date_data.between_time(range_start_time, range_end_time, inclusive="left")

        print(f"Data for {date}:")
        print(date_range_data)

        # Calculate the highest high and lowest low within the specified time range
        if not date_range_data.empty:
            highest_high = date_range_data["mid_h"].max()
            lowest_low = date_range_data["mid_l"].min()

            print(GREEN + f"Highest High in the specified time range: {highest_high}" + RESET)
            print(GREEN + f"Lowest Low in the specified time range: {lowest_low}" + RESET)

            # Check if the price first closes above or below the range after the range end time and in the same day
            end_time = pd.Timestamp(date).replace(hour=int(range_end_time[:2]), minute=int(range_end_time[3:]),
                                                  second=0, microsecond=0)
            eastern_tz = pytz.timezone('US/Eastern')
            end_time = eastern_tz.localize(end_time)

            after_range_end = date_data[date_data.index >= end_time]

            if not after_range_end.empty:
                above_high_after_range = after_range_end[after_range_end["mid_c"] > highest_high]
                below_low_after_range = after_range_end[after_range_end["mid_c"] < lowest_low]

                if not above_high_after_range.empty:
                    first_close_above_high_time = above_high_after_range.index[0]
                    print(
                        YELLOW + f"First close above highest high after range end time at: {first_close_above_high_time}" + RESET)

                    # Separate the data into two parts based on the closing condition
                    after_above_high = date_data[date_data.index > first_close_above_high_time]
                    after_below_low = date_data[date_data.index > after_range_end.index[-1]]

                    # Check if price trades into 50% of the range after closing above the range
                    fifty_percent_level = ((highest_high - lowest_low) / 2.0) + lowest_low
                    trade_into_range = False  # Initialize the variable
                    trade_into_50_percent_time = None  # Initialize the variable to store the time

                    for _, row in after_above_high.iterrows():
                        if row["mid_l"] <= fifty_percent_level:
                            trade_into_range = True
                            trade_into_50_percent_time = row.name
                            break

                    if trade_into_range:
                        print(
                            BLUE + f"Price trades into 50% of the range after closing above the range at: {trade_into_50_percent_time}. Price: {row['mid_c']}" + RESET)
                    else:
                        print(RED + "Price did not trade into 50% of the range after closing above the range." + RESET)

                if not below_low_after_range.empty:
                    first_close_below_low_time = below_low_after_range.index[0]
                    print(
                        YELLOW + f"First close below lowest low after range end time at: {first_close_below_low_time}" + RESET)

                    # Separate the data into two parts based on the closing condition
                    after_below_low = date_data[date_data.index > first_close_below_low_time]
                    after_above_high = date_data[date_data.index > after_range_end.index[-1]]

                    # Check if price trades into 50% of the range after closing below the range
                    fifty_percent_level = ((highest_high - lowest_low) / 2.0) + lowest_low
                    trade_into_range = False  # Initialize the variable
                    trade_into_50_percent_time = None  # Initialize the variable to store the time

                    for _, row in after_below_low.iterrows():
                        if row["mid_h"] >= fifty_percent_level:
                            trade_into_range = True
                            trade_into_50_percent_time = row.name
                            break

                    if trade_into_range:
                        print(
                            BLUE + f"Price trades into 50% of the range after closing below the range at: {trade_into_50_percent_time}. Price: {row['mid_c']}" + RESET)
                    else:
                        print(RED + "Price did not trade into 50% of the range after closing below the range." + RESET)

        print("\n")



SPX: OandaAPI = OandaAPI()
data : DataFrame = SPX.create_data("SPX500_USD", "M15")
print(data)

backtesting_dr(data, "9:30", "10:30")