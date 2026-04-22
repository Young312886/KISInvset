"""
기업 펀더멘털 분석 서비스 (Phase 2 핵심 모듈)

OpenDARTReader를 활용하여 재무제표 데이터를 수집하고,
S-RIM 적정 주가 계산 및 퀀트 지표를 산출합니다.
"""
import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from ..core.config import settings
from ..repositories.fundamental_repository import FundamentalsRepository

logger = logging.getLogger(__name__)


def _safe_divide(numerator, denominator, default=None):
    """0으로 나누기 방지 유틸리티"""
    if denominator and denominator != 0:
        return numerator / denominator
    return default


class DartService:
    """
    OpenDARTReader를 활용한 재무 데이터 수집 서비스.
    
    OpenDARTReader: https://github.com/FinanceData/OpenDartReader
    사용 전 반드시 .env에 DART_API_KEY를 설정하세요.
    발급: https://opendart.fss.or.kr/
    """

    def __init__(self):
        self.api_key = settings.DART_API_KEY
        self._dart = None  # Lazy initialization

    def _get_dart_client(self):
        """OpenDartReader 클라이언트를 지연 초기화합니다."""
        if self._dart is None:
            if not self.api_key:
                raise ValueError(
                    "DART_API_KEY가 설정되지 않았습니다. "
                    ".env 파일에 DART_API_KEY를 추가해주세요. "
                    "(발급: https://opendart.fss.or.kr/)"
                )
            try:
                import OpenDartReader
                self._dart = OpenDartReader.OpenDartReader(self.api_key)
                logger.info("OpenDartReader 클라이언트 초기화 성공.")
            except ImportError:
                raise ImportError(
                    "OpenDartReader가 설치되지 않았습니다. "
                    "'pip install OpenDartReader'를 실행하세요."
                )
        return self._dart

    def fetch_financial_statements(self, ticker: str, fiscal_year: int) -> Optional[Dict[str, Any]]:
        """
        특정 종목의 연간 재무제표 주요 항목을 수집합니다.
        
        Args:
            ticker: 종목 코드 (예: '005930' for 삼성전자)
            fiscal_year: 회계연도 (예: 2024)
        
        Returns:
            재무제표 원시 데이터 딕셔너리, 실패 시 None
        """
        dart = self._get_dart_client()
        
        try:
            # 연간 재무제표(CFS: 연결, OFS: 개별) 가져오기
            # fs_div='CFS' (연결재무제표) 우선 사용
            finstate = dart.finstate_all(ticker, str(fiscal_year), fs_div='CFS')
            
            if finstate is None or finstate.empty:
                logger.warning(f"[{ticker}] {fiscal_year}년 연결재무제표 없음. 개별재무제표 시도...")
                finstate = dart.finstate_all(ticker, str(fiscal_year), fs_div='OFS')
            
            if finstate is None or finstate.empty:
                logger.error(f"[{ticker}] {fiscal_year}년 재무제표 데이터를 가져올 수 없습니다.")
                return None

            # --- 주요 계정 추출 ---
            def get_value(account_nm: str, column: str = 'thstrm_amount') -> Optional[float]:
                """계정명으로 값을 추출하는 내부 함수"""
                row = finstate[finstate['account_nm'].str.contains(account_nm, na=False)]
                if not row.empty:
                    try:
                        val = row.iloc[0][column]
                        return float(str(val).replace(',', '')) if val and val != '-' else None
                    except (ValueError, TypeError):
                        return None
                return None

            revenue = get_value('매출액')
            operating_profit = get_value('영업이익')
            net_income = get_value('당기순이익')
            total_assets = get_value('자산총계')
            total_equity = get_value('자본총계')
            total_debt = get_value('부채총계')
            
            # 전년도 데이터 (성장률 계산용)
            prev_revenue = get_value('매출액', 'frmtrm_amount')
            prev_operating_profit = get_value('영업이익', 'frmtrm_amount')

            return {
                "revenue": revenue,
                "operating_profit": operating_profit,
                "net_income": net_income,
                "total_assets": total_assets,
                "total_equity": total_equity,
                "total_debt": total_debt,
                "prev_revenue": prev_revenue,
                "prev_operating_profit": prev_operating_profit,
            }

        except Exception as e:
            logger.error(f"[{ticker}] DART 데이터 수집 오류: {e}")
            return None

    def fetch_company_info(self, ticker: str) -> Optional[Dict[str, str]]:
        """종목의 기본 정보(회사명, 시장)를 가져옵니다."""
        dart = self._get_dart_client()
        try:
            company = dart.company(ticker)
            if company is not None and not company.empty:
                return {
                    "company_name": company.get('corp_name', [None])[0],
                    "market": company.get('stock_market', [None])[0],  # '유가증권' or '코스닥'
                }
        except Exception as e:
            logger.error(f"[{ticker}] 회사 정보 조회 오류: {e}")
        return None


class SRimService:
    """
    S-RIM (사경인 회계사 방식) 적정 주가 계산 서비스.
    
    공식: 적정주가 = BPS + Σ(초과이익 / (1+r)^n)
    - BPS: 주당순자산 (자기자본 / 발행주식수)
    - 초과이익 = EPS - (전기 BPS × 요구수익률)
    - r: 요구수익률 (일반적으로 BBB+ 회사채 수익률 사용, 현재 약 4~5% 수준)
    - n: 예측 기간 (보통 10년)
    """

    DEFAULT_DISCOUNT_RATE = 0.045  # 4.5% (BBB+ 회사채 기준)
    FORECAST_YEARS = 10

    def calculate(
        self,
        bps: float,          # 주당순자산 (BPS)
        roe: float,          # 자기자본이익률 (소수점, 예: 0.15 = 15%)
        discount_rate: Optional[float] = None,
        forecast_years: int = FORECAST_YEARS
    ) -> Dict[str, float]:
        """
        S-RIM 방식으로 적정 주가를 계산합니다.
        
        Args:
            bps: 주당순자산가치 (원)
            roe: 자기자본이익률 (소수점 형태, 예: 0.15)
            discount_rate: 요구수익률 (소수점, 기본값: BBB+ 회사채 수익률)
            forecast_years: 초과이익 예측 기간 (기본: 10년)
        
        Returns:
            {
                "intrinsic_value": 적정 주가 (원),
                "discount_rate": 사용된 할인율,
                "excess_profit_pv": 초과이익의 현재가치 합계,
            }
        """
        if discount_rate is None:
            discount_rate = self.DEFAULT_DISCOUNT_RATE

        current_bps = bps
        total_excess_profit_pv = 0.0

        for year in range(1, forecast_years + 1):
            # 해당 연도의 EPS = 전기 BPS × ROE
            eps_forecast = current_bps * roe
            # 요구이익 = 전기 BPS × 요구수익률(할인율)
            required_profit = current_bps * discount_rate
            # 초과이익 = EPS - 요구이익
            excess_profit = eps_forecast - required_profit
            # 초과이익의 현재가치 = 초과이익 / (1 + r)^n
            pv = excess_profit / ((1 + discount_rate) ** year)
            total_excess_profit_pv += pv
            # BPS 갱신 (자본 재투자 가정)
            current_bps += eps_forecast

        intrinsic_value = bps + total_excess_profit_pv

        return {
            "intrinsic_value": round(intrinsic_value, 2),
            "discount_rate": discount_rate,
            "excess_profit_pv": round(total_excess_profit_pv, 2),
        }


class FundamentalAnalysisService:
    """
    통합 펀더멘털 분석 서비스.
    DART 데이터 수집 → 지표 계산 → DB 저장을 담당합니다.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = FundamentalsRepository(db)
        self.dart_service = DartService()
        self.srim_service = SRimService()

    def calculate_and_save_fundamentals(
        self, ticker: str, fiscal_year: int, current_price: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        특정 종목의 재무 데이터를 수집, 계산하여 DB에 저장합니다.
        
        Args:
            ticker: 종목 코드
            fiscal_year: 회계연도
            current_price: 현재 주가 (PER, PBR 등 시장가치 지표 계산에 필요)
        """
        logger.info(f"[{ticker}] 펀더멘털 분석 시작 (회계연도: {fiscal_year})")

        # 1. DART에서 재무제표 원시 데이터 수집
        raw_data = self.dart_service.fetch_financial_statements(ticker, fiscal_year)
        if not raw_data:
            return {"error": f"[{ticker}] DART 재무 데이터를 가져올 수 없습니다."}

        company_info = self.dart_service.fetch_company_info(ticker) or {}

        revenue = raw_data.get("revenue")
        operating_profit = raw_data.get("operating_profit")
        net_income = raw_data.get("net_income")
        total_assets = raw_data.get("total_assets")
        total_equity = raw_data.get("total_equity")
        total_debt = raw_data.get("total_debt")

        # 2. 주요 지표 계산
        roe = _safe_divide(net_income, total_equity)
        roa = _safe_divide(net_income, total_assets)
        operating_margin = _safe_divide(operating_profit, revenue)
        net_profit_margin = _safe_divide(net_income, revenue)
        debt_ratio = _safe_divide(total_debt, total_equity)

        # GP/A (매출총이익 ≈ 영업이익으로 근사, 실제로는 별도 계산 필요)
        gpa = _safe_divide(operating_profit, total_assets)

        # 성장률 (전년 대비)
        prev_revenue = raw_data.get("prev_revenue")
        revenue_growth_yoy = _safe_divide(
            (revenue - prev_revenue) if (revenue and prev_revenue) else None,
            prev_revenue
        )

        prev_op = raw_data.get("prev_operating_profit")
        op_growth_yoy = _safe_divide(
            (operating_profit - prev_op) if (operating_profit and prev_op) else None,
            prev_op
        )

        # 3. S-RIM 적정 주가 계산 (BPS 필요 → 주식 수로 나눠야 하나, 여기서는 자기자본 기준)
        srim_result = {}
        # NOTE: 실제 BPS는 발행주식수로 나눠야 함 (KIS API에서 별도 조회 필요)
        # 현재는 자기자본을 BPS 대용으로 사용하는 단순화 버전
        if total_equity and roe:
            # 총 자기자본 기준 S-RIM (발행주식수 데이터가 없는 경우 대용)
            roe_decimal = roe if roe < 1 else roe / 100
            srim_result = self.srim_service.calculate(
                bps=total_equity,
                roe=roe_decimal,
            )

        # 4. DB 저장용 데이터 구성
        fundamentals_data = {
            "ticker_symbol": ticker,
            "company_name": company_info.get("company_name"),
            "market": company_info.get("market"),
            "roe": round(roe * 100, 4) if roe else None,  # % 변환
            "roa": round(roa * 100, 4) if roa else None,
            "operating_margin": round(operating_margin * 100, 4) if operating_margin else None,
            "net_profit_margin": round(net_profit_margin * 100, 4) if net_profit_margin else None,
            "gpa": round(gpa * 100, 4) if gpa else None,
            "debt_ratio": round(debt_ratio * 100, 2) if debt_ratio else None,
            "revenue_growth_yoy": round(revenue_growth_yoy * 100, 4) if revenue_growth_yoy else None,
            "operating_profit_growth_yoy": round(op_growth_yoy * 100, 4) if op_growth_yoy else None,
            "revenue": int(revenue) if revenue else None,
            "operating_profit": int(operating_profit) if operating_profit else None,
            "net_income": int(net_income) if net_income else None,
            "total_assets": int(total_assets) if total_assets else None,
            "total_equity": int(total_equity) if total_equity else None,
            "total_debt": int(total_debt) if total_debt else None,
            "srim_intrinsic_value": srim_result.get("intrinsic_value"),
            "srim_discount_rate": srim_result.get("discount_rate"),
            "srim_equity_per_share": total_equity,  # 임시: 실제 BPS는 KIS API 별도 조회 필요
            "fiscal_year": fiscal_year,
            "data_source": "DART",
        }

        # 5. PER, PBR 등 시장가치 지표 (현재 주가가 있는 경우)
        if current_price and total_equity and net_income:
            eps = net_income  # 임시: 실제 EPS는 발행주식수 필요
            fundamentals_data["eps"] = eps

        saved = self.repo.upsert_fundamentals(fundamentals_data)
        logger.info(f"[{ticker}] 펀더멘털 데이터 저장 완료.")
        return fundamentals_data

    def get_fundamentals(self, ticker: str) -> Optional[dict]:
        """특정 종목의 저장된 펀더멘털 데이터를 조회합니다."""
        record = self.repo.get_by_ticker(ticker)
        if not record:
            return None
        return record

    def screen_stocks(self, criteria: dict) -> List:
        """퀀트 기준으로 종목을 스크리닝합니다."""
        return self.repo.screen_by_criteria(**criteria)


class ScoringService:
    """
    Value-Trend 복합 스코어링 서비스.
    펀더멘털 점수와 기술적 분석 시그널을 결합합니다.
    """

    def calculate_fundamental_score(self, fundamentals: dict) -> Dict[str, float]:
        """
        재무 지표를 기반으로 각 영역별 점수(0~100)와 종합 점수를 계산합니다.
        점수 기준은 한국 주식 시장의 평균적인 기준값을 사용합니다.
        """
        scores = {}

        # --- 1. 수익성 점수 (ROE, 영업이익률) ---
        roe = fundamentals.get("roe") or 0
        op_margin = fundamentals.get("operating_margin") or 0
        profitability = min(100, max(0,
            (min(roe, 30) / 30 * 60) +  # ROE: 30% 이상이면 만점 (60점 비중)
            (min(op_margin, 20) / 20 * 40)  # 영업이익률: 20% 이상 만점 (40점 비중)
        ))
        scores["profitability_score"] = round(profitability, 2)

        # --- 2. 가치 점수 (PBR 저평가 여부 + S-RIM 할인율) ---
        pbr = fundamentals.get("pbr") or 999
        per = fundamentals.get("per") or 999
        srim_value = fundamentals.get("srim_intrinsic_value")

        valuation_score = 50  # 기본값
        if pbr < 1.0:
            valuation_score = 100
        elif pbr < 1.5:
            valuation_score = 80
        elif pbr < 2.5:
            valuation_score = 60
        elif pbr < 4.0:
            valuation_score = 40
        else:
            valuation_score = 20
        scores["valuation_score"] = round(valuation_score, 2)

        # --- 3. 성장성 점수 (매출 및 영업이익 성장률) ---
        rev_growth = fundamentals.get("revenue_growth_yoy") or 0
        op_growth = fundamentals.get("operating_profit_growth_yoy") or 0
        growth = min(100, max(0,
            (min(max(rev_growth, 0), 30) / 30 * 50) +
            (min(max(op_growth, 0), 30) / 30 * 50)
        ))
        scores["growth_score"] = round(growth, 2)

        # --- 4. 안전성 점수 (부채비율) ---
        debt_ratio = fundamentals.get("debt_ratio") or 999
        if debt_ratio < 50:
            safety = 100
        elif debt_ratio < 100:
            safety = 80
        elif debt_ratio < 150:
            safety = 60
        elif debt_ratio < 200:
            safety = 40
        else:
            safety = 20
        scores["safety_score"] = round(safety, 2)

        # --- 5. 배당 매력도 점수 ---
        div_yield = fundamentals.get("dividend_yield") or 0
        dividend = min(100, div_yield / 5 * 100)  # 5% 이상이면 만점
        scores["dividend_score"] = round(dividend, 2)

        # --- 종합 펀더멘털 점수 (가중 평균) ---
        weights = {
            "profitability_score": 0.30,
            "valuation_score": 0.30,
            "growth_score": 0.20,
            "safety_score": 0.15,
            "dividend_score": 0.05,
        }
        total = sum(scores.get(k, 0) * v for k, v in weights.items())
        scores["fundamental_score"] = round(total, 2)

        return scores

    def calculate_total_score(self, fundamental_score: float, technical_signal: str) -> Dict[str, Any]:
        """
        펀더멘털 점수(70%)와 기술적 시그널(30%)을 결합하여 최종 점수를 계산합니다.
        """
        # 기술적 시그널을 점수로 변환
        signal_score_map = {
            "STRONG_BUY": 100,
            "BUY": 75,
            "HOLD": 50,
            "SELL": 25,
            "STRONG_SELL": 0,
        }
        tech_score = signal_score_map.get(technical_signal, 50)

        total = (fundamental_score * 0.70) + (tech_score * 0.30)

        if total >= 80:
            recommendation = "STRONG_BUY"
        elif total >= 65:
            recommendation = "BUY"
        elif total >= 45:
            recommendation = "HOLD"
        else:
            recommendation = "AVOID"

        return {
            "total_score": round(total, 2),
            "recommendation": recommendation,
            "technical_score": tech_score,
        }
