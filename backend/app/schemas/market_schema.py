from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockPrice(BaseModel):
    symbol: str
    current_price: float
    change: float
    change_rate: float
    volume: int
    high: float
    low: float
    open: float
    last_updated: Optional[str] = None
    error: Optional[str] = None
