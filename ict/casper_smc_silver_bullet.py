import pandas as pd
import time

def is_bullish_fair_value_gap(prev_row, next_row):
    return (
            prev_row["mid_h"] < next_row["mid_l"]
    )

def is_bearish_fair_value_gap(prev_row, next_row):
    return (
            prev_row["mid_l"] > next_row["mid_h"]
    )

def fair_value_gap_strategy(df):
    balance = 100000  # Initial balance
    risk_percent = 0.01  # Risk percentage per trade
    rr = 2  # Reward-to-risk ratio

    for idx, middle_candle in df.iterrows():
        if pd.Timestamp("10:00").time() <= middle_candle.name.time() < pd.Timestamp("11:00").time():
            prev_candle = df.shift(1).loc[idx]
            next_candle = df.shift(-1).loc[idx]

            if prev_candle is not None and next_candle is not None:
                # Bullish fair value gap
                if middle_candle["mid_c"] > middle_candle["mid_o"] and is_bullish_fair_value_gap(prev_candle, next_candle):

                    fair_value_gap_time = middle_candle.name
                    print(f"Fair value gap is occurring at {fair_value_gap_time}")

                    fair_value_gap_high = next_candle["mid_l"]
                    stop_loss = prev_candle["mid_l"]
                    take_profit = fair_value_gap_high + (fair_value_gap_high - stop_loss) * rr

                    entry_price = fair_value_gap_high
                    trade_type = "SELL"

                # Bearish fair value gap
                elif middle_candle["mid_c"] < middle_candle["mid_o"] and is_bearish_fair_value_gap(prev_candle, next_candle):

                    fair_value_gap_time = middle_candle.name
                    print(f"Fair value gap is occurring at {fair_value_gap_time}")

                    fair_value_gap_low = next_candle["mid_h"]
                    stop_loss = prev_candle["mid_h"]
                    take_profit = fair_value_gap_low - (stop_loss - fair_value_gap_low) * rr

                    entry_price = fair_value_gap_low
                    trade_type = "BUY"

                print(f"Fair Value Gap {trade_type} Trade:")
                print(f"Entry Price: {entry_price}")
                print(f"Stop Loss: {stop_loss}")
                print(f"Take Profit: {take_profit}")

                if trade_type == "SELL":
                    if take_profit > entry_price:
                        print("Invalid trade setup: Take Profit is higher than entry price.")
                        continue
                elif trade_type == "BUY":
                    if take_profit < entry_price:
                        print("Invalid trade setup: Take Profit is lower than entry price.")
                        continue

                # Simulate trade execution and update balance
                if trade_type == "SELL":
                    balance -= balance * risk_percent
                    if stop_loss >= entry_price:
                        balance -= balance * risk_percent
                    elif take_profit <= entry_price:
                        balance += balance * risk_percent
                elif trade_type == "BUY":
                    balance -= balance * risk_percent
                    if stop_loss <= entry_price:
                        balance -= balance * risk_percent
                    elif take_profit >= entry_price:
                        balance += balance * risk_percent

                print(f"New balance: {balance}\n")

