from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from ..api.kis_api import KISApi
from ..core.analysis.ichimoku import calculate_ichimoku
from ..repositories.signal_repository import AnalysisSignalRepository

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.kis_api = KISApi()
        self.signal_repo = AnalysisSignalRepository(db)

    def get_ichimoku_data(self, symbol: str, timeframe: str) -> dict:
        """Fetches data and calculates Ichimoku, returns data for charting."""
        ohlcv_df = self.kis_api.fetch_ohlcv(symbol, timeframe=timeframe[0].upper())
        if ohlcv_df.empty:
            return {"error": "Could not fetch OHLCV data."}

        ichimoku_df = calculate_ichimoku(ohlcv_df)
        
        # Convert NaN to None for JSON compatibility
        ichimoku_df = ichimoku_df.replace({np.nan: None})
        
        # Reset index to make 'date' a regular column
        ichimoku_df = ichimoku_df.reset_index()

        return ichimoku_df.to_dict(orient='records')

    def generate_signal(self, symbol: str, timeframe: str) -> dict:
        # 1. Fetch data
        ohlcv_df = self.kis_api.fetch_ohlcv(symbol, timeframe=timeframe[0].upper())
        if ohlcv_df.empty:
            return {"error": "Could not fetch OHLCV data."}

        # 2. Calculate Ichimoku
        ichimoku_df = calculate_ichimoku(ohlcv_df)
        
        # Get the last two data points for crossover detection
        last_two = ichimoku_df.dropna(subset=['tenkan_sen', 'kijun_sen']).tail(2)
        if len(last_two) < 2:
            return {"error": "Not enough data to generate a signal."}
            
        prev = last_two.iloc[0]
        last = last_two.iloc[1]

        # 3. Generate Signal (Simple Crossover Logic)
        signal = "HOLD"
        # Golden Cross
        if prev['tenkan_sen'] < prev['kijun_sen'] and last['tenkan_sen'] > last['kijun_sen']:
            signal = "BUY"
        # Dead Cross
        elif prev['tenkan_sen'] > prev['kijun_sen'] and last['tenkan_sen'] < last['kijun_sen']:
            signal = "SELL"

        # 4. Save Signal
        signal_data = {
            "symbol": symbol,
            "timeframe": timeframe,
            "signal": signal,
            "details": {
                "tenkan_sen": last['tenkan_sen'],
                "kijun_sen": last['kijun_sen'],
                "senkou_span_a": last['senkou_span_a'],
                "senkou_span_b": last['senkou_span_b'],
                "close": last['close']
            }
        }
        
        created_signal = self.signal_repo.create_signal(signal_data)
        return created_signal
