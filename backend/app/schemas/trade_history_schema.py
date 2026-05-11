from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class TradeHistoryBase(BaseModel):
    symbol: str
    company_name: Optional[str] = None
    trade_type: str  # 'BUY' or 'SELL'
    quantity: int
    price: Decimal
    commission: Decimal = Field(default=Decimal('0.00'))
    tax: Decimal = Field(default=Decimal('0.00'))
    memo: Optional[str] = None

class TradeHistoryCreate(TradeHistoryBase):
    account_id: int

class TradeHistory(TradeHistoryBase):
    id: int
    account_id: int
    traded_at: datetime

    class Config:
        from_attributes = True
