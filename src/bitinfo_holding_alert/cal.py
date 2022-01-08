"""Transform time series to actionable timeframe."""
import pandas as pd


def infer_col(df_holding_ts: pd.DataFrame) -> pd.DataFrame:
    """
    1. extract balance value -> convert to float
    2. convert datetime col
    """
    regex_str = '(.*)\s.*'
    df_holding_ts["Balance"] = df_holding_ts["Balance"].str.extract(regex_str, expand=False)
    df_holding_ts["Balance"] = df_holding_ts["Balance"].str.replace(',', '').astype(float)

    df_holding_ts["Time"] = pd.to_datetime(df_holding_ts["Time"], format="%Y-%m-%d %H:%M:%S")
    df_holding_ts = df_holding_ts.set_index("Time").sort_index()
    return df_holding_ts


def resample_balance(df_holding_ts: pd.DataFrame, timeframe: str) -> pd.Series:
    balance_ts = df_holding_ts["Balance"].resample(timeframe, label='right', closed='right').last()
    balance_ts = balance_ts.ffill()
    return balance_ts


def produce_time_series(df_holding_ts: pd.DataFrame, timeframe: str, sma: int) -> pd.Series:
    df_holding_ts = infer_col(df_holding_ts)
    balance_ts = resample_balance(df_holding_ts, timeframe)
    balance_ts = balance_ts.rolling(window=sma).mean()
    return balance_ts
