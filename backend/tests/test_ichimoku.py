import pytest
import pandas as pd
import numpy as np
from app.core.analysis.ichimoku import calculate_ichimoku

def test_calculate_ichimoku_basic():
    # Create mock OHLCV dataframe (at least 52 periods required for Senkou Span B)
    # Using 60 rows of dummy data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=60, freq='D')
    
    # Generate prices with a slight upward trend
    base_price = 100
    closes = base_price + np.cumsum(np.random.randn(60) * 2)
    highs = closes + np.abs(np.random.randn(60) * 2)
    lows = closes - np.abs(np.random.randn(60) * 2)
    opens = closes - (closes - lows) * 0.5
    volumes = np.random.randint(1000, 10000, size=60)
    
    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes
    }, index=dates)
    
    result_df = calculate_ichimoku(df)
    
    # Check if necessary columns are created
    expected_columns = ['tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']
    for col in expected_columns:
        assert col in result_df.columns, f"Missing column: {col}"
        
    # Check length
    # Note: calculate_ichimoku might shift the dataframe (extending it by 26 periods for future cloud)
    assert len(result_df) >= 60
    
    # Tenkan-sen is 9 periods High-Low average
    # The 9th row should have a tenkan_sen value (index 8)
    assert not pd.isna(result_df['tenkan_sen'].iloc[8])
    assert pd.isna(result_df['tenkan_sen'].iloc[7]) # First 8 rows should be NaN for Tenkan
    
    # Kijun-sen is 26 periods
    assert not pd.isna(result_df['kijun_sen'].iloc[25])
    assert pd.isna(result_df['kijun_sen'].iloc[24])

def test_calculate_ichimoku_empty_df():
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
    result_df = calculate_ichimoku(df)
    assert result_df.empty
