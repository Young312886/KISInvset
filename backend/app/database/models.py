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
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("KisAccount", back_populates="owner")

class KisAccount(Base):
    __tablename__ = "kis_accounts"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    account_number = Column(String, unique=True, index=True, nullable=False)
    app_key_encrypted = Column(String, nullable=False)
    app_secret_encrypted = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="accounts")
    assets = relationship("Asset", back_populates="account")
    trade_history = relationship("TradeHistory", back_populates="account")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(BigInteger, primary_key=True, index=True)
    account_id = Column(BigInteger, ForeignKey("kis_accounts.id"))
    symbol = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    avg_purchase_price = Column(DECIMAL(18, 2), nullable=False)
    last_updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    account = relationship("KisAccount", back_populates="assets")

class TradeHistory(Base):
    __tablename__ = "trade_history"
    id = Column(BigInteger, primary_key=True, index=True)
    account_id = Column(BigInteger, ForeignKey("kis_accounts.id"))
    symbol = Column(String, index=True, nullable=False)
    trade_type = Column(String, nullable=False)  # 'BUY' or 'SELL'
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    traded_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("KisAccount", back_populates="trade_history")

class OhlcvData(Base):
    __tablename__ = "ohlcv_data"
    id = Column(BigInteger, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String, index=True) # '1D', '4H'
    candle_time = Column(DateTime(timezone=True), index=True)
    open = Column(DECIMAL(18, 2))
    high = Column(DECIMAL(18, 2))
    low = Column(DECIMAL(18, 2))
    close = Column(DECIMAL(18, 2))
    volume = Column(BigInteger)

class AnalysisSignal(Base):
    __tablename__ = "analysis_signals"
    id = Column(BigInteger, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)
    signal = Column(String) # 'STRONG_BUY', 'BUY', 'HOLD', 'SELL', 'STRONG_SELL'
    details = Column(JSON)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
