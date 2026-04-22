from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    BigInteger,
    DECIMAL,
    JSON,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .connection import Base


# =============================================================================
# 사용자 관련 (User & Auth)
# =============================================================================

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    accounts = relationship("KisAccount", back_populates="owner")
    watchlist = relationship("WatchlistItem", back_populates="user")


class KisAccount(Base):
    __tablename__ = "kis_accounts"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    account_number = Column(String(50), unique=True, index=True, nullable=False)
    # API 키는 Fernet 암호화 후 저장
    app_key_encrypted = Column(Text, nullable=False)
    app_secret_encrypted = Column(Text, nullable=False)
    account_type = Column(String(20), default="MOCK")  # 'MOCK' or 'REAL'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="accounts")
    assets = relationship("Asset", back_populates="account")
    trade_history = relationship("TradeHistory", back_populates="account")


# =============================================================================
# 포트폴리오 및 자산 관리 (Portfolio & Ledger)
# =============================================================================

class Asset(Base):
    __tablename__ = "assets"

    id = Column(BigInteger, primary_key=True, index=True)
    account_id = Column(BigInteger, ForeignKey("kis_accounts.id"), nullable=False)
    symbol = Column(String(20), index=True, nullable=False)
    company_name = Column(String(100))
    quantity = Column(Integer, nullable=False, default=0)
    avg_purchase_price = Column(DECIMAL(18, 2), nullable=False)
    last_updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    account = relationship("KisAccount", back_populates="assets")
    __table_args__ = (UniqueConstraint("account_id", "symbol", name="uq_account_symbol"),)


class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(BigInteger, primary_key=True, index=True)
    account_id = Column(BigInteger, ForeignKey("kis_accounts.id"), nullable=False)
    symbol = Column(String(20), index=True, nullable=False)
    company_name = Column(String(100))
    trade_type = Column(String(10), nullable=False)  # 'BUY' or 'SELL'
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    # 수수료 및 세금
    commission = Column(DECIMAL(18, 2), default=0)
    tax = Column(DECIMAL(18, 2), default=0)
    traded_at = Column(DateTime(timezone=True), server_default=func.now())
    memo = Column(Text)

    account = relationship("KisAccount", back_populates="trade_history")


class WatchlistItem(Base):
    """사용자 관심 종목 목록"""
    __tablename__ = "watchlist"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), index=True, nullable=False)
    company_name = Column(String(100))
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="watchlist")
    __table_args__ = (UniqueConstraint("user_id", "symbol", name="uq_user_symbol"),)


# =============================================================================
# 기술적 분석 데이터 (Technical Analysis)
# =============================================================================

class OhlcvData(Base):
    __tablename__ = "ohlcv_data"

    id = Column(BigInteger, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    timeframe = Column(String(10), index=True, nullable=False)  # '1D', '4H', '1H', etc.
    candle_time = Column(DateTime(timezone=True), index=True, nullable=False)
    open = Column(DECIMAL(18, 2))
    high = Column(DECIMAL(18, 2))
    low = Column(DECIMAL(18, 2))
    close = Column(DECIMAL(18, 2))
    volume = Column(BigInteger)

    __table_args__ = (
        UniqueConstraint("symbol", "timeframe", "candle_time", name="uq_ohlcv"),
    )


class AnalysisSignal(Base):
    __tablename__ = "analysis_signals"

    id = Column(BigInteger, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    timeframe = Column(String(10), index=True)
    # 기술적 시그널: 'STRONG_BUY', 'BUY', 'HOLD', 'SELL', 'STRONG_SELL'
    signal = Column(String(20), nullable=False)
    # 근거가 된 지표값들을 JSON으로 저장
    details = Column(JSON)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())


# =============================================================================
# 펀더멘털 분석 데이터 (Fundamental Analysis) - [NEW]
# =============================================================================

class CompanyFundamentals(Base):
    """
    기업 펀더멘털(재무) 정보 테이블.
    OpenDARTReader를 통해 정기적으로(배치) 갱신됩니다.
    """
    __tablename__ = "company_fundamentals"

    id = Column(BigInteger, primary_key=True, index=True)
    ticker_symbol = Column(String(20), unique=True, index=True, nullable=False)
    company_name = Column(String(100))
    market = Column(String(10))  # 'KOSPI', 'KOSDAQ'

    # --- 수익성 지표 (Profitability) ---
    roe = Column(DECIMAL(10, 4))           # 자기자본이익률 (%)
    roa = Column(DECIMAL(10, 4))           # 총자산이익률 (%)
    operating_margin = Column(DECIMAL(10, 4))  # 영업이익률 (%)
    net_profit_margin = Column(DECIMAL(10, 4)) # 순이익률 (%)
    gpa = Column(DECIMAL(10, 4))           # GP/A: 매출총이익 / 총자산 (로버트 노비-막스 지표)

    # --- 가치 지표 (Valuation) ---
    per = Column(DECIMAL(10, 2))           # 주가수익비율
    pbr = Column(DECIMAL(10, 2))           # 주가순자산비율
    psr = Column(DECIMAL(10, 2))           # 주가매출비율
    pcr = Column(DECIMAL(10, 2))           # 주가현금흐름비율
    ev_ebitda = Column(DECIMAL(10, 2))     # EV/EBITDA

    # --- 성장성 지표 (Growth) ---
    revenue_growth_yoy = Column(DECIMAL(10, 4))        # 매출 전년 대비 성장률 (%)
    operating_profit_growth_yoy = Column(DECIMAL(10, 4)) # 영업이익 전년 대비 성장률 (%)
    eps_growth_yoy = Column(DECIMAL(10, 4))            # EPS 전년 대비 성장률 (%)

    # --- 안전성 지표 (Safety) ---
    debt_ratio = Column(DECIMAL(10, 2))    # 부채비율 (%)
    current_ratio = Column(DECIMAL(10, 2)) # 유동비율 (%)
    interest_coverage = Column(DECIMAL(10, 2))  # 이자보상배율

    # --- 활동성 지표 (Activity) ---
    asset_turnover = Column(DECIMAL(10, 4))  # 총자산회전율

    # --- 배당 지표 (Dividend) ---
    dividend_yield = Column(DECIMAL(10, 4))  # 배당수익률 (%)
    dividend_payout_ratio = Column(DECIMAL(10, 4))  # 배당성향 (%)

    # --- S-RIM 가치 평가 (Absolute Valuation) ---
    srim_intrinsic_value = Column(DECIMAL(18, 2))  # S-RIM 적정 주가
    srim_discount_rate = Column(DECIMAL(10, 4))    # 적용된 할인율 (BBB+ 회사채 수익률 등)
    srim_equity_per_share = Column(DECIMAL(18, 2)) # 주당 자기자본 (BPS)

    # --- 원시 재무 데이터 (Raw Financials for calculation) ---
    revenue = Column(BigInteger)           # 매출액 (원)
    operating_profit = Column(BigInteger)  # 영업이익 (원)
    net_income = Column(BigInteger)        # 당기순이익 (원)
    total_assets = Column(BigInteger)      # 총자산 (원)
    total_equity = Column(BigInteger)      # 자기자본 (원)
    total_debt = Column(BigInteger)        # 총부채 (원)
    eps = Column(DECIMAL(18, 2))           # 주당순이익

    # --- 메타 데이터 ---
    fiscal_year = Column(Integer)          # 기준 회계연도 (e.g., 2024)
    data_source = Column(String(20), default="DART")  # 데이터 출처
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 관계: 해당 종목의 가장 최근 복합 시그널 스코어
    value_trend_scores = relationship("ValueTrendScore", back_populates="fundamentals",
                                       foreign_keys="ValueTrendScore.ticker_symbol",
                                       primaryjoin="CompanyFundamentals.ticker_symbol == ValueTrendScore.ticker_symbol")


class ValueTrendScore(Base):
    """
    Value-Trend 스코어링 결과 테이블.
    재무 건강도(펀더멘털)와 기술적 시그널(일목)을 결합한 종합 점수를 저장합니다.
    """
    __tablename__ = "value_trend_scores"

    id = Column(BigInteger, primary_key=True, index=True)
    ticker_symbol = Column(String(20), ForeignKey("company_fundamentals.ticker_symbol"), index=True, nullable=False)
    
    # --- 세부 점수 (각 0~100점) ---
    fundamental_score = Column(Float)    # 펀더멘털 종합 점수
    profitability_score = Column(Float)  # 수익성 점수
    valuation_score = Column(Float)      # 가치 점수 (저평가 여부)
    growth_score = Column(Float)         # 성장성 점수
    safety_score = Column(Float)         # 안전성 점수
    dividend_score = Column(Float)       # 배당 매력도 점수

    # --- 기술적 시그널 정보 ---
    technical_signal = Column(String(20))  # 가장 최근 일목균형표 시그널
    is_above_kumo = Column(Boolean)        # 구름대 위에 있는지 여부 (True=상승 추세)
    is_golden_cross = Column(Boolean)      # 전환선/기준선 골든크로스 여부

    # --- 종합 점수 ---
    total_score = Column(Float)          # 종합 스코어 (Value-Trend Score)
    recommendation = Column(String(20))  # 'STRONG_BUY', 'BUY', 'HOLD', 'AVOID'

    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    fundamentals = relationship("CompanyFundamentals", back_populates="value_trend_scores",
                                  foreign_keys=[ticker_symbol])
