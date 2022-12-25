from dr_trade_simulation import *

if __name__ == "__main__":
    exec(open('dr_trade_simulation.py').read())
    daily = OandaAPI()
    daily.create_data("SPX500_USD", "D")

    daily_df: DataFrame = daily.df.copy()

    daily_df = add_dr_bias(dr_bias, daily_df)

    daily_df['daily_candle_close'] = daily_df.apply(evaluate_daily_candle_close, axis=1)

    print(daily_df.tail(50))

