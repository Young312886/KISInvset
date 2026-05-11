from sqlalchemy.orm import Session
from ..database.models import WatchlistItem
from typing import List

class WatchlistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_watchlist(self, user_id: int) -> List[WatchlistItem]:
        return self.db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id).all()

    def add_to_watchlist(self, user_id: int, symbol: str, company_name: str = None) -> WatchlistItem:
        item = WatchlistItem(user_id=user_id, symbol=symbol, company_name=company_name)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def remove_from_watchlist(self, user_id: int, symbol: str) -> bool:
        item = self.db.query(WatchlistItem).filter(
            WatchlistItem.user_id == user_id, 
            WatchlistItem.symbol == symbol
        ).first()
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False
