from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.backtest_service import BacktestService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/backtest", tags=["backtest"])

@router.get("/run")
async def run_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    initial_cash: float = 10000000.0,
    strategy: str = 'sma_crossover',
    backtest_service: BacktestService = Depends(BacktestService)
):
    """
    Run a historical backtest for a stock.
    Example: /backtest/run?symbol=005930&start_date=20230101&end_date=20231231
    """
    result = await backtest_service.run_backtest(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        initial_cash=initial_cash,
        strategy_name=strategy
    )
    return result
