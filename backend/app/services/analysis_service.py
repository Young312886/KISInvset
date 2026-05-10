from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from ..api.kis_api import KISApi
from ..core.analysis.ichimoku import calculate_ichimoku
from ..core.analysis.resample import resample_ohlcv
from ..repositories.signal_repository import AnalysisSignalRepository

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.kis_api = KISApi()
        self.signal_repo = AnalysisSignalRepository(db)

    def get_ichimoku_data(self, symbol: str, timeframe: str) -> dict:
        """Fetches data and calculates Ichimoku, returns data for charting."""
        if timeframe.endswith('H') or timeframe.endswith('T') or timeframe.endswith('min'):
            # Intraday timeframe
            ohlcv_df = self.kis_api.fetch_minute_ohlcv(symbol)
            ohlcv_df = resample_ohlcv(ohlcv_df, timeframe)
        else:
            # Daily, Weekly, Monthly
            ohlcv_df = self.kis_api.fetch_ohlcv(symbol, timeframe=timeframe[0].upper())
            
        if ohlcv_df is None or ohlcv_df.empty:
            return {"error": "Could not fetch OHLCV data."}

        ichimoku_df = calculate_ichimoku(ohlcv_df)
        
        # Convert NaN to None for JSON compatibility
        ichimoku_df = ichimoku_df.replace({np.nan: None})
        
        # Reset index to make 'date' a regular column
        ichimoku_df = ichimoku_df.reset_index()

        return ichimoku_df.to_dict(orient='records')

    def generate_signal(self, symbol: str, timeframe: str) -> dict:
        # 1. Fetch data
        if timeframe.endswith('H') or timeframe.endswith('T') or timeframe.endswith('min'):
            ohlcv_df = self.kis_api.fetch_minute_ohlcv(symbol)
            ohlcv_df = resample_ohlcv(ohlcv_df, timeframe)
        else:
            ohlcv_df = self.kis_api.fetch_ohlcv(symbol, timeframe=timeframe[0].upper())
            
        if ohlcv_df is None or ohlcv_df.empty:
            return {"error": "Could not fetch OHLCV data."}

        # 2. Calculate Ichimoku
        ichimoku_df = calculate_ichimoku(ohlcv_df)
        
        # Get the last two data points for crossover detection
        last_two = ichimoku_df.dropna(subset=['tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b']).tail(2)
        if len(last_two) < 2:
            return {"error": "Not enough data to generate a signal."}
            
        prev = last_two.iloc[0]
        last = last_two.iloc[1]

        # 3. Generate Signal (Complex Logic)
        signal = "HOLD"
        reasons = []

        # 3.1. 전환선/기준선 교차 (Tenkan / Kijun Crossover)
        is_tk_cross_up = prev['tenkan_sen'] <= prev['kijun_sen'] and last['tenkan_sen'] > last['kijun_sen']
        is_tk_cross_down = prev['tenkan_sen'] >= prev['kijun_sen'] and last['tenkan_sen'] < last['kijun_sen']
        
        if is_tk_cross_up:
            reasons.append("전환선이 기준선을 상향 돌파 (호전)")
        elif is_tk_cross_down:
            reasons.append("전환선이 기준선을 하향 돌파 (역전)")

        # 3.2. 구름대 돌파 (Cloud Breakout)
        prev_cloud_top = max(prev['senkou_span_a'], prev['senkou_span_b'])
        prev_cloud_bottom = min(prev['senkou_span_a'], prev['senkou_span_b'])
        last_cloud_top = max(last['senkou_span_a'], last['senkou_span_b'])
        last_cloud_bottom = min(last['senkou_span_a'], last['senkou_span_b'])

        is_cloud_break_up = prev['close'] <= prev_cloud_top and last['close'] > last_cloud_top
        is_cloud_break_down = prev['close'] >= prev_cloud_bottom and last['close'] < last_cloud_bottom

        if is_cloud_break_up:
            reasons.append("주가가 구름대를 상향 돌파")
        elif is_cloud_break_down:
            reasons.append("주가가 구름대를 하향 돌파")

        # 3.3. 후행스팬 호전/역전 (Chikou Span)
        chikou_period = 26
        if len(ichimoku_df) > chikou_period:
            past_close = ichimoku_df['close'].iloc[-chikou_period-1]
            if last['close'] > past_close:
                reasons.append("후행스팬 호전 (현재 주가가 26일 전 주가 상회)")
            elif last['close'] < past_close:
                reasons.append("후행스팬 역전")

        # 3.4. 종합 시그널 판정 (3역 호전 / 3역 역전)
        is_price_above_cloud = last['close'] > last_cloud_top
        is_price_below_cloud = last['close'] < last_cloud_bottom
        is_chikou_up = len(ichimoku_df) > chikou_period and last['close'] > ichimoku_df['close'].iloc[-chikou_period-1]
        is_chikou_down = len(ichimoku_df) > chikou_period and last['close'] < ichimoku_df['close'].iloc[-chikou_period-1]

        if last['tenkan_sen'] > last['kijun_sen'] and is_price_above_cloud and is_chikou_up:
            signal = "STRONG_BUY"
        elif is_tk_cross_up or is_cloud_break_up:
            signal = "BUY"
        elif last['tenkan_sen'] < last['kijun_sen'] and is_price_below_cloud and is_chikou_down:
            signal = "STRONG_SELL"
        elif is_tk_cross_down or is_cloud_break_down:
            signal = "SELL"

        # 4. Save Signal
        signal_data = {
            "symbol": symbol,
            "timeframe": timeframe,
            "signal": signal,
            "details": {
                "reasons": reasons,
                "tenkan_sen": last['tenkan_sen'],
                "kijun_sen": last['kijun_sen'],
                "senkou_span_a": last['senkou_span_a'],
                "senkou_span_b": last['senkou_span_b'],
                "close": last['close']
            }
        }
        
        created_signal = self.signal_repo.create_signal(signal_data)
        return created_signal
