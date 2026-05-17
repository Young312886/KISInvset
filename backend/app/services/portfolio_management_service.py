import pandas as pd
import numpy as np
from ..api.kis_api import KISApi

class PortfolioManagementService:
    def __init__(self):
        self.api = KISApi()

    def calculate_kelly_criterion(self, win_rate: float, win_loss_ratio: float, fraction: float = 0.5) -> float:
        """
        Calculates the recommended position size using the Kelly Criterion.
        win_rate: Probability of winning (0.0 to 1.0)
        win_loss_ratio: Average profit of winning trades / Average loss of losing trades
        fraction: Half-Kelly or Fractional Kelly is commonly used in practice to reduce volatility.
        Returns the percentage of the portfolio to allocate.
        """
        if win_rate <= 0 or win_loss_ratio <= 0:
            return 0.0

        kelly_pct = win_rate - ((1 - win_rate) / win_loss_ratio)
        
        # Apply fractional Kelly and ensure it's between 0 and 1
        recommended_pct = max(0.0, min(1.0, kelly_pct * fraction))
        return recommended_pct

    def detect_market_regime(self, market_symbol: str = '0001') -> dict:
        """
        Detects the current market regime based on KOSPI (or other index) moving averages.
        market_symbol: Default is '0001' (often used for KOSPI index in KIS API)
        """
        try:
            # Fetch at least 200 days of data for the index
            # Using daily timeframe
            df = self.api.fetch_ohlcv(market_symbol, timeframe='D')
            if df is None or df.empty or len(df) < 200:
                return {
                    "regime": "UNKNOWN",
                    "technical_weight": 0.5,
                    "fundamental_weight": 0.5,
                    "message": "Not enough data to detect market regime."
                }
            
            # Calculate SMAs
            df['sma_50'] = df['close'].rolling(window=50).mean()
            df['sma_200'] = df['close'].rolling(window=200).mean()
            
            last_row = df.iloc[-1]
            current_price = last_row['close']
            sma_50 = last_row['sma_50']
            sma_200 = last_row['sma_200']
            
            regime = "SIDEWAYS"
            technical_weight = 0.5
            fundamental_weight = 0.5
            
            if current_price > sma_50 and sma_50 > sma_200:
                regime = "BULL"
                technical_weight = 0.7
                fundamental_weight = 0.3
            elif current_price < sma_50 and sma_50 < sma_200:
                regime = "BEAR"
                technical_weight = 0.3
                fundamental_weight = 0.7
                
            return {
                "regime": regime,
                "technical_weight": technical_weight,
                "fundamental_weight": fundamental_weight,
                "indicators": {
                    "current_price": current_price,
                    "sma_50": sma_50,
                    "sma_200": sma_200
                }
            }
        except Exception as e:
            return {
                "regime": "ERROR",
                "technical_weight": 0.5,
                "fundamental_weight": 0.5,
                "message": str(e)
            }
