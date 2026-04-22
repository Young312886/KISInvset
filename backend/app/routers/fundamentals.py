"""
기업 펀더멘털 분석 API 라우터.

엔드포인트:
  - POST /fundamentals/{ticker}/collect    : DART에서 특정 종목 재무 데이터 수집 및 저장
  - GET  /fundamentals/{ticker}            : 특정 종목의 저장된 재무 데이터 조회
  - GET  /fundamentals/                    : 전체 종목 재무 데이터 조회 (시장 필터 가능)
  - POST /fundamentals/screen              : 퀀트 조건 기반 종목 스크리닝
  - GET  /fundamentals/{ticker}/score      : Value-Trend 복합 점수 조회
  - POST /fundamentals/{ticker}/score/calculate : Value-Trend 점수 재계산
"""
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.fundamental_schema import (
    FundamentalsResponse,
    ValueTrendScoreResponse,
    ScreeningRequest,
)
from ..services.fundamental_service import FundamentalAnalysisService, ScoringService
from ..repositories.fundamental_repository import FundamentalsRepository, ValueTrendScoreRepository

router = APIRouter()


@router.post("/{ticker}/collect", summary="종목 재무 데이터 수집 (DART)")
def collect_fundamentals(
    ticker: str,
    fiscal_year: int = Query(default=datetime.datetime.now().year - 1, description="회계연도 (기본: 전년도)"),
    current_price: Optional[float] = Query(default=None, description="현재 주가 (PER/PBR 계산용)"),
    db: Session = Depends(get_db),
):
    """
    DART API를 통해 특정 종목의 재무제표를 수집하고 DB에 저장합니다.
    
    - **ticker**: 종목 코드 (예: 005930)
    - **fiscal_year**: 수집할 회계연도 (기본값: 전년도)
    - **current_price**: 현재 주가 (시장 가치 지표 계산 시 필요, 옵션)
    
    > ⚠️ DART API 키(.env의 DART_API_KEY)가 반드시 설정되어 있어야 합니다.
    """
    service = FundamentalAnalysisService(db)
    result = service.calculate_and_save_fundamentals(ticker, fiscal_year, current_price)
    if result and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": f"[{ticker}] 펀더멘털 데이터 수집 완료", "data": result}


@router.get("/{ticker}", response_model=FundamentalsResponse, summary="종목 재무 데이터 조회")
def get_fundamentals(ticker: str, db: Session = Depends(get_db)):
    """
    DB에 저장된 특정 종목의 재무 데이터를 조회합니다.
    데이터가 없으면 먼저 `/collect` 엔드포인트를 호출하세요.
    """
    repo = FundamentalsRepository(db)
    record = repo.get_by_ticker(ticker)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"[{ticker}] 재무 데이터가 없습니다. POST /{ticker}/collect 를 먼저 실행하세요."
        )
    return record


@router.get("/", response_model=List[FundamentalsResponse], summary="전체 종목 재무 데이터 목록")
def list_fundamentals(
    market: Optional[str] = Query(default=None, description="시장 필터 (KOSPI/KOSDAQ)"),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """DB에 저장된 전체 종목의 재무 데이터를 조회합니다."""
    repo = FundamentalsRepository(db)
    return repo.get_all(market=market, limit=limit)


@router.post("/screen", summary="퀀트 조건 기반 종목 스크리닝")
def screen_stocks(request: ScreeningRequest, db: Session = Depends(get_db)):
    """
    재무 조건과 기술적 시그널 조건을 복합적으로 사용하여 종목을 필터링합니다.
    
    **예시**: ROE > 10% AND PBR < 1.5 AND 구름대 위에 있는 종목
    """
    repo = FundamentalsRepository(db)
    score_repo = ValueTrendScoreRepository(db)

    # 1단계: 재무 기준 필터링
    fundamental_results = repo.screen_by_criteria(
        min_roe=request.min_roe,
        max_pbr=request.max_pbr,
        max_per=request.max_per,
        max_debt_ratio=request.max_debt_ratio,
        min_dividend_yield=request.min_dividend_yield,
        market=request.market,
        limit=200,  # 넉넉하게 조회 후 기술적 조건으로 재필터
    )

    tickers = [f.ticker_symbol for f in fundamental_results]

    # 2단계: 기술적 시그널 조건 필터링 (Value-Trend 스코어 있는 경우)
    if request.require_above_kumo or request.require_golden_cross or request.min_total_score:
        top_scores = score_repo.get_top_scores(
            min_total_score=request.min_total_score,
            require_above_kumo=request.require_above_kumo,
            require_golden_cross=request.require_golden_cross,
            limit=200,
        )
        score_tickers = {s.ticker_symbol for s in top_scores}
        tickers = [t for t in tickers if t in score_tickers]

    return {
        "count": len(tickers[:request.limit]),
        "tickers": tickers[:request.limit],
        "criteria": request.model_dump(),
    }


@router.get("/{ticker}/score", response_model=ValueTrendScoreResponse, summary="Value-Trend 점수 조회")
def get_value_trend_score(ticker: str, db: Session = Depends(get_db)):
    """특정 종목의 Value-Trend 복합 점수를 조회합니다."""
    repo = ValueTrendScoreRepository(db)
    score = repo.get_by_ticker(ticker)
    if not score:
        raise HTTPException(
            status_code=404,
            detail=f"[{ticker}] Value-Trend 점수가 없습니다. POST /{ticker}/score/calculate 를 실행하세요."
        )
    return score


@router.post("/{ticker}/score/calculate", summary="Value-Trend 점수 계산 및 저장")
def calculate_value_trend_score(
    ticker: str,
    technical_signal: str = Query(default="HOLD", description="기술적 시그널 (STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL)"),
    is_above_kumo: bool = Query(default=False, description="구름대 위 여부"),
    is_golden_cross: bool = Query(default=False, description="골든크로스 여부"),
    db: Session = Depends(get_db),
):
    """
    저장된 펀더멘털 데이터와 입력받은 기술적 시그널을 결합하여
    Value-Trend 복합 점수를 계산하고 DB에 저장합니다.
    """
    # 펀더멘털 데이터 조회
    fund_repo = FundamentalsRepository(db)
    fundamentals = fund_repo.get_by_ticker(ticker)
    if not fundamentals:
        raise HTTPException(
            status_code=404,
            detail=f"[{ticker}] 재무 데이터 없음. POST /{ticker}/collect 를 먼저 실행하세요."
        )

    # 점수 계산
    scoring = ScoringService()
    fund_scores = scoring.calculate_fundamental_score(fundamentals.__dict__)
    combined = scoring.calculate_total_score(fund_scores["fundamental_score"], technical_signal)

    # DB 저장
    score_data = {
        "ticker_symbol": ticker,
        **fund_scores,
        "technical_signal": technical_signal,
        "is_above_kumo": is_above_kumo,
        "is_golden_cross": is_golden_cross,
        **combined,
    }

    score_repo = ValueTrendScoreRepository(db)
    saved_score = score_repo.upsert_score(score_data)

    return {
        "message": f"[{ticker}] Value-Trend 점수 계산 완료",
        "score": score_data,
    }
