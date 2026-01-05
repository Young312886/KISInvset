from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SignalRequest(BaseModel):
    symbol: str
    timeframe: str = 'D' # Default to daily

class Signal(BaseModel):
    id: int
    symbol: str
    timeframe: str
    signal: str
    details: Optional[Dict[str, Any]] = None
    generated_at: datetime

    class Config:
        from_attributes = True # orm_mode = True
