import pytest
import pandas as pd
from app.services.backtest_service import BacktestService

@pytest.mark.asyncio
async def test_run_backtest_metrics(mocker):
    service = BacktestService()
    
    # Mock data: 30 days of data
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    prices = [100, 105, 110, 108, 115, 120, 118, 125, 130, 128, 135, 140, 138, 145, 150, 
              148, 155, 160, 158, 165, 170, 168, 175, 180, 178, 185, 190, 188, 195, 200]
    df = pd.DataFrame({'close': prices}, index=dates)
    
    mocker.patch.object(service.api, 'fetch_ohlcv', return_value=df)
    
    # Run backtest
    result = await service.run_backtest('005930', '2023-01-01', '2023-01-30')
    
    assert "symbol" in result
    assert result["symbol"] == '005930'
    assert "win_rate" in result
    assert "sharpe_ratio" in result
    assert "benchmark_return_pct" in result
    assert "history" in result
    assert "trades" in result
    
    assert result["benchmark_return_pct"] == 100.0 # (200 - 100) / 100 * 100
    
    if len(result["trades"]) > 0:
        for trade in result["trades"]:
            assert "type" in trade
            assert "price" in trade
            assert "quantity" in trade
            if trade["type"] == "SELL":
                assert "profit" in trade
                assert "profit_pct" in trade
