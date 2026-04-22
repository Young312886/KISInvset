from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FundamentalsBase(BaseModel):
    ticker_symbol: str
    company_name: Optional[str] = None
    market: Optional[str] = None
    # 수익성
    roe: Optional[float] = None
    roa: Optional[float] = None
    operating_margin: Optional[float] = None
    net_profit_margin: Optional[float] = None
    gpa: Optional[float] = None
    # 가치
    per: Optional[float] = None
    pbr: Optional[float] = None
    psr: Optional[float] = None
    ev_ebitda: Optional[float] = None
    # 성장성
    revenue_growth_yoy: Optional[float] = None
    operating_profit_growth_yoy: Optional[float] = None
    eps_growth_yoy: Optional[float] = None
    # 안전성
    debt_ratio: Optional[float] = None
    current_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    # 배당
    dividend_yield: Optional[float] = None
    dividend_payout_ratio: Optional[float] = None
    # S-RIM
    srim_intrinsic_value: Optional[float] = None
    srim_discount_rate: Optional[float] = None
    srim_equity_per_share: Optional[float] = None
    # 원시 재무
    eps: Optional[float] = None
    fiscal_year: Optional[int] = None


class FundamentalsResponse(FundamentalsBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class ValueTrendScoreResponse(BaseModel):
    id: int
    ticker_symbol: str
    fundamental_score: Optional[float] = None
    profitability_score: Optional[float] = None
    valuation_score: Optional[float] = None
    growth_score: Optional[float] = None
    safety_score: Optional[float] = None
    dividend_score: Optional[float] = None
    technical_signal: Optional[str] = None
    is_above_kumo: Optional[bool] = None
    is_golden_cross: Optional[bool] = None
    total_score: Optional[float] = None
    recommendation: Optional[str] = None
    scored_at: datetime

    class Config:
        from_attributes = True


class ScreeningRequest(BaseModel):
    """멀티 팩터 스크리닝 요청 파라미터"""
    min_roe: Optional[float] = None           # 최소 ROE (%)
    max_pbr: Optional[float] = None           # 최대 PBR
    max_per: Optional[float] = None           # 최대 PER
    max_debt_ratio: Optional[float] = None    # 최대 부채비율 (%)
    min_dividend_yield: Optional[float] = None # 최소 배당수익률 (%)
    require_above_kumo: bool = False           # 구름대 위 종목만 필터
    require_golden_cross: bool = False         # 골든크로스 종목만 필터
    min_total_score: Optional[float] = None   # 최소 Value-Trend 점수
    market: Optional[str] = None              # 'KOSPI', 'KOSDAQ', None=전체
    limit: int = 20                           # 결과 개수 제한
