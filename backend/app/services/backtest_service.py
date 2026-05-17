import pandas as pd
import numpy as np
from typing import List, Dict, Any, Callable
from app.api.kis_api import KISApi

class BacktestService:
    def __init__(self):
        self.api = KISApi()

    async def run_backtest(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str, 
        initial_cash: float = 10000000.0,
        strategy_name: str = 'sma_crossover'
    ) -> Dict[str, Any]:
        """
        Runs a backtest for a given symbol and strategy.
        """
        df = self.api.fetch_ohlcv(symbol, timeframe='D', end_date=end_date)
        if df.empty:
            return {"error": "No data found for the given symbol and period"}

        # Filter by start date
        df = df[df.index >= pd.to_datetime(start_date)]
        
        if len(df) < 20:
            return {"error": "Not enough data points for backtesting (minimum 20 days)"}

        # Apply strategy signals
        if strategy_name == 'sma_crossover':
            df = self._sma_crossover_strategy(df)
        elif strategy_name == 'rsi':
            df = self._rsi_strategy(df)
        else:
            return {"error": f"Unknown strategy: {strategy_name}"}

        # Simulation
        cash = initial_cash
        shares = 0
        portfolio_history = []
        trades = []

        for date, row in df.iterrows():
            signal = row.get('signal', 0)
            price = row['close']

            if signal == 1 and cash >= price: # Buy signal
                shares_to_buy = int(cash // price)
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    cash -= cost
                    shares += shares_to_buy
                    trades.append({
                        "date": date.strftime('%Y-%m-%d'),
                        "type": "BUY",
                        "price": price,
                        "quantity": shares_to_buy,
                        "cost": cost
                    })
            
            elif signal == -1 and shares > 0: # Sell signal
                revenue = shares * price
                cash += revenue
                
                # Find matching buy to calculate profit
                last_buy = next((t for t in reversed(trades) if t["type"] == "BUY"), None)
                profit = revenue - (shares * last_buy["price"]) if last_buy else 0
                profit_pct = (profit / (shares * last_buy["price"])) if last_buy else 0
                
                trades.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "type": "SELL",
                    "price": price,
                    "quantity": shares,
                    "revenue": revenue,
                    "profit": profit,
                    "profit_pct": profit_pct
                })
                shares = 0

            current_value = cash + (shares * price)
            portfolio_history.append({
                "date": date.strftime('%Y-%m-%d'),
                "portfolio_value": current_value,
                "close": price
            })

        final_value = cash + (shares * df.iloc[-1]['close'])
        total_return = ((final_value - initial_cash) / initial_cash) * 100
        
        # Calculate Benchmark Return
        initial_price = df.iloc[0]['close']
        final_price = df.iloc[-1]['close']
        benchmark_return_pct = ((final_price - initial_price) / initial_price) * 100

        # Calculate MDD
        values = [p['portfolio_value'] for p in portfolio_history]
        peak = np.maximum.accumulate(values)
        drawdown = (values - peak) / peak
        mdd = np.min(drawdown) * 100
        
        # Calculate Win Rate
        sell_trades = [t for t in trades if t["type"] == "SELL"]
        winning_trades = [t for t in sell_trades if t.get("profit", 0) > 0]
        win_rate = (len(winning_trades) / len(sell_trades)) * 100 if sell_trades else 0
        
        # Calculate Sharpe Ratio
        df_history = pd.DataFrame(portfolio_history)
        df_history['daily_return'] = df_history['portfolio_value'].pct_change()
        risk_free_rate = 0.035 / 252 # Assumed 3.5% annual risk-free rate
        excess_returns = df_history['daily_return'] - risk_free_rate
        sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / excess_returns.std()) if excess_returns.std() > 0 else 0

        return {
            "symbol": symbol,
            "initial_cash": initial_cash,
            "final_value": final_value,
            "total_return_pct": total_return,
            "benchmark_return_pct": benchmark_return_pct,
            "mdd_pct": mdd,
            "win_rate": win_rate,
            "sharpe_ratio": float(sharpe_ratio),
            "trades_count": len(trades),
            "history": portfolio_history,
            "trades": trades
        }

    def _sma_crossover_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['sma_fast'] = df['close'].rolling(window=5).mean()
        df['sma_slow'] = df['close'].rolling(window=20).mean()
        
        df['signal'] = 0
        # Buy when fast > slow, Sell when fast < slow
        df.loc[df['sma_fast'] > df['sma_slow'], 'signal'] = 1
        df.loc[df['sma_fast'] < df['sma_slow'], 'signal'] = -1
        
        # Only keep changes in signal
        df['signal'] = df['signal'].diff().fillna(0)
        df.loc[df['signal'] > 0, 'signal'] = 1
        df.loc[df['signal'] < 0, 'signal'] = -1
        
        return df

    def _rsi_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        df['signal'] = 0
        # Buy when RSI < 30 (oversold), Sell when RSI > 70 (overbought)
        df.loc[df['rsi'] < 30, 'signal'] = 1
        df.loc[df['rsi'] > 70, 'signal'] = -1
        
        return df
