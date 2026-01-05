import pandas as pd

def calculate_ichimoku(df: pd.DataFrame):
    """
    Calculates the five components of the Ichimoku Cloud.    
    Args:
        df (pd.DataFrame): DataFrame with 'high', 'low', 'close' columns.        
    Returns:
        pd.DataFrame: The original DataFrame with Ichimoku lines appended.
    """
    # 1. Tenkan-sen (Conversion Line)
    tenkan_period = 9
    tenkan_high = df['high'].rolling(window=tenkan_period).max()
    tenkan_low = df['low'].rolling(window=tenkan_period).min()
    df['tenkan_sen'] = (tenkan_high + tenkan_low) / 2

    # 2. Kijun-sen (Base Line)
    kijun_period = 26
    kijun_high = df['high'].rolling(window=kijun_period).max()
    kijun_low = df['low'].rolling(window=kijun_period).min()
    df['kijun_sen'] = (kijun_high + kijun_low) / 2

    # 3. Senkou Span A (Leading Span A)
    # This is the average of Tenkan-sen and Kijun-sen, plotted 26 periods ahead.
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(kijun_period)

    # 4. Senkou Span B (Leading Span B)
    # This is the average of the highest high and lowest low over the past 52 periods, plotted 26 periods ahead.
    senkou_b_period = 52
    senkou_b_high = df['high'].rolling(window=senkou_b_period).max()
    senkou_b_low = df['low'].rolling(window=senkou_b_period).min()
    df['senkou_span_b'] = ((senkou_b_high + senkou_b_low) / 2).shift(kijun_period)

    # 5. Chikou Span (Lagging Span)
    # This is the current closing price, plotted 26 periods behind.
    df['chikou_span'] = df['close'].shift(-kijun_period)
    
    return df

if __name__ == '__main__':
    # Example usage for testing the calculation
    data = {
        'high': [i for i in range(100, 200)],
        'low': [i for i in range(90, 190)],
        'close': [i for i in range(95, 195)]
    }
    test_df = pd.DataFrame(data)
    
    ichimoku_df = calculate_ichimoku(test_df.copy())
    
    print("Ichimoku Calculation Test")
    print(ichimoku_df.tail(10))
    
    # Check specific values
    print("\nSample calculated values (last row):")
    print(f"Tenkan-sen: {ichimoku_df['tenkan_sen'].iloc[-1]}")
    print(f"Kijun-sen: {ichimoku_df['kijun_sen'].iloc[-1]}")
    print(f"Senkou Span A (shifted): {ichimoku_df['senkou_span_a'].iloc[-27]}") # Check pre-shift value
    print(f"Senkou Span B (shifted): {ichimoku_df['senkou_span_b'].iloc[-27]}") # Check pre-shift value
    print(f"Chikou Span (shifted): {ichimoku_df['chikou_span'].iloc[-27]}") # Check pre-shift value
