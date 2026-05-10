import pandas as pd

def resample_ohlcv(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resamples minute-level OHLCV data to a higher timeframe.
    
    Args:
        df (pd.DataFrame): DataFrame with a datetime index and 'open', 'high', 'low', 'close', 'volume' columns.
        timeframe (str): Pandas offset alias (e.g., '4H' for 4 hours, '1H' for 1 hour, '15T' for 15 minutes).
        
    Returns:
        pd.DataFrame: Resampled DataFrame.
    """
    if df.empty:
        return df

    # Ensure the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception as e:
            raise ValueError(f"Index must be convertible to DatetimeIndex for resampling. Error: {e}")

    # Define aggregation rules for OHLCV
    ohlcv_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    # Resample and drop rows with all NaNs (periods with no trading)
    resampled_df = df.resample(timeframe).agg(ohlcv_dict).dropna(how='all')
    
    return resampled_df
