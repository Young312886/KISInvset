from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from ..database import get_db
from ..schemas import signal_schema
from ..services.analysis_service import AnalysisService
from ..repositories.signal_repository import AnalysisSignalRepository

router = APIRouter()

@router.post("/generate", response_model=signal_schema.Signal)
def generate_new_signal(
    request: signal_schema.SignalRequest, 
    db: Session = Depends(get_db)
):
    """
    Triggers a new analysis for a given stock symbol and timeframe,
    saves the result, and returns the generated signal.
    """
    service = AnalysisService(db)
    result = service.generate_signal(symbol=request.symbol, timeframe=request.timeframe)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.get("/{symbol}", response_model=signal_schema.Signal)
def get_latest_signal_for_symbol(
    symbol: str,
    timeframe: str = 'D',
    db: Session = Depends(get_db)
):
    """
    Retrieves the most recently generated signal for a given stock symbol and timeframe.
    """
    repo = AnalysisSignalRepository(db)
    signal = repo.get_latest_signal(symbol=symbol, timeframe=timeframe)
    
    if not signal:
        raise HTTPException(status_code=404, detail="No signal found for this symbol and timeframe.")
        
    return signal

@router.get("/{symbol}/chart", response_model=List[Dict[str, Any]])
def get_chart_data(
    symbol: str,
    timeframe: str = 'D',
    db: Session = Depends(get_db)
):
    """
    Retrieves the full OHLCV and Ichimoku data for charting.
    """
    service = AnalysisService(db)
    result = service.get_ichimoku_data(symbol=symbol, timeframe=timeframe)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result
