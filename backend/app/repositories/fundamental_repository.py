from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from ..database.models import CompanyFundamentals, ValueTrendScore


class FundamentalsRepository:
    """기업 펀더멘털 데이터 CRUD"""

    def __init__(self, db: Session):
        self.db = db

    def upsert_fundamentals(self, data: dict) -> CompanyFundamentals:
        """
        ticker_symbol 기준으로 데이터가 있으면 UPDATE, 없으면 INSERT.
        (배치 수집 시 사용)
        """
        ticker = data.get("ticker_symbol")
        existing = self.db.query(CompanyFundamentals).filter(
            CompanyFundamentals.ticker_symbol == ticker
        ).first()

        if existing:
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            record = CompanyFundamentals(**data)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record

    def get_by_ticker(self, ticker_symbol: str) -> Optional[CompanyFundamentals]:
        return self.db.query(CompanyFundamentals).filter(
            CompanyFundamentals.ticker_symbol == ticker_symbol
        ).first()

    def get_all(self, market: Optional[str] = None, limit: int = 100) -> List[CompanyFundamentals]:
        query = self.db.query(CompanyFundamentals)
        if market:
            query = query.filter(CompanyFundamentals.market == market)
        return query.limit(limit).all()

    def screen_by_criteria(
        self,
        min_roe: Optional[float] = None,
        max_pbr: Optional[float] = None,
        max_per: Optional[float] = None,
        max_debt_ratio: Optional[float] = None,
        min_dividend_yield: Optional[float] = None,
        market: Optional[str] = None,
        limit: int = 20,
    ) -> List[CompanyFundamentals]:
        """재무 조건 기반 종목 스크리닝"""
        query = self.db.query(CompanyFundamentals)

        if market:
            query = query.filter(CompanyFundamentals.market == market)
        if min_roe is not None:
            query = query.filter(CompanyFundamentals.roe >= min_roe)
        if max_pbr is not None:
            query = query.filter(CompanyFundamentals.pbr <= max_pbr)
        if max_per is not None:
            query = query.filter(
                CompanyFundamentals.per <= max_per,
                CompanyFundamentals.per > 0  # 적자 기업 제외
            )
        if max_debt_ratio is not None:
            query = query.filter(CompanyFundamentals.debt_ratio <= max_debt_ratio)
        if min_dividend_yield is not None:
            query = query.filter(CompanyFundamentals.dividend_yield >= min_dividend_yield)

        return query.limit(limit).all()


class ValueTrendScoreRepository:
    """Value-Trend 복합 스코어 CRUD"""

    def __init__(self, db: Session):
        self.db = db

    def upsert_score(self, data: dict) -> ValueTrendScore:
        """ticker_symbol 기준으로 스코어를 갱신합니다."""
        ticker = data.get("ticker_symbol")
        existing = self.db.query(ValueTrendScore).filter(
            ValueTrendScore.ticker_symbol == ticker
        ).first()

        if existing:
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            record = ValueTrendScore(**data)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record

    def get_top_scores(
        self,
        min_total_score: Optional[float] = None,
        require_above_kumo: bool = False,
        require_golden_cross: bool = False,
        limit: int = 20,
    ) -> List[ValueTrendScore]:
        """Value-Trend 점수 기준 상위 종목 조회"""
        query = self.db.query(ValueTrendScore)

        if min_total_score is not None:
            query = query.filter(ValueTrendScore.total_score >= min_total_score)
        if require_above_kumo:
            query = query.filter(ValueTrendScore.is_above_kumo == True)
        if require_golden_cross:
            query = query.filter(ValueTrendScore.is_golden_cross == True)

        return query.order_by(desc(ValueTrendScore.total_score)).limit(limit).all()

    def get_by_ticker(self, ticker_symbol: str) -> Optional[ValueTrendScore]:
        return self.db.query(ValueTrendScore).filter(
            ValueTrendScore.ticker_symbol == ticker_symbol
        ).first()
