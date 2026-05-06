from sqlalchemy.orm import Session
from ..database.models import AnalysisSignal
from ..schemas.signal_schema import Signal

class AnalysisSignalRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_signal(self, signal_data: dict) -> AnalysisSignal:
        db_signal = AnalysisSignal(**signal_data)
        self.db.add(db_signal)
        self.db.commit()
        self.db.refresh(db_signal)
        return db_signal

    def get_latest_signal(self, symbol: str, timeframe: str) -> AnalysisSignal:
        return self.db.query(AnalysisSignal).filter(
            AnalysisSignal.symbol == symbol,
            AnalysisSignal.timeframe == timeframe
        ).order_by(AnalysisSignal.generated_at.desc()).first()

