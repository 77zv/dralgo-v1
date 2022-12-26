from dr_trade_simulation import *

if __name__ == "__main__":
    exec(open('dr_trade_simulation.py').read())
    daily = OandaAPI()
    daily.create_data("SPX500_USD", "D")

    daily_df: DataFrame = daily.df.copy()
    # removing columns I don't need
    daily_df.drop(['mid_h', 'mid_l'], axis=1, inplace=True)

    daily_df = add_dr_bias(dr_bias, daily_df)

    daily_df['daily_close'] = daily_df.apply(evaluate_daily_candle_close, axis=1)
    daily_df['test_dr_bias'] = daily_df.apply(test_bias, axis=1)
    daily_df.dropna(inplace=True)

    print(daily_df)
    print(f"In the last {daily_df.shape[0]} days, the Defining Range had a {  daily_df['test_dr_bias'].sum() / daily_df.shape[0]* 100}% accuracy rate in predicting the daily bias")