from sqlalchemy.orm import Session
from ..database.models import TradeHistory
from ..schemas.trade_history_schema import TradeHistoryCreate

class TradeHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_account(self, account_id: int, limit: int = 10):
        return self.db.query(TradeHistory)\
            .filter(TradeHistory.account_id == account_id)\
            .order_by(TradeHistory.traded_at.desc())\
            .limit(limit)\
            .all()

    def create(self, trade: TradeHistoryCreate):
        db_trade = TradeHistory(**trade.model_dump())
        self.db.add(db_trade)
        self.db.commit()
        self.db.refresh(db_trade)
        return db_trade

    def get_all_by_user(self, user_id: int, limit: int = 20):
        # Join with KisAccount to filter by user_id
        from ..database.models import KisAccount
        return self.db.query(TradeHistory)\
            .join(KisAccount)\
            .filter(KisAccount.user_id == user_id)\
            .order_by(TradeHistory.traded_at.desc())\
            .limit(limit)\
            .all()
