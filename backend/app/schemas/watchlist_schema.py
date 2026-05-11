from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WatchlistItemBase(BaseModel):
    symbol: str
    company_name: Optional[str] = None

class WatchlistItemCreate(WatchlistItemBase):
    pass

class WatchlistItem(WatchlistItemBase):
    id: int
    user_id: int
    added_at: datetime

    class Config:
        from_attributes = True
