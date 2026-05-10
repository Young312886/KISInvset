import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import WatchlistItem, Asset
from app.services.fundamental_service import FundamentalAnalysisService

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def update_fundamentals_job():
    """매일 장 마감 후 실행되는 펀더멘털 데이터 갱신 배치 작업"""
    logger.info("--- [배치 작업] 관심 종목 펀더멘털 데이터 갱신 시작 ---")
    db: Session = SessionLocal()
    try:
        # 관심 종목(Watchlist) 및 보유 자산(Asset)에 등록된 모든 고유 심볼 조회
        watchlist_symbols = db.query(WatchlistItem.symbol).all()
        asset_symbols = db.query(Asset.symbol).all()
        
        # 고유 심볼 추출
        symbols = set([s[0] for s in watchlist_symbols] + [s[0] for s in asset_symbols])
        
        if not symbols:
            logger.info("갱신할 관심 종목이나 보유 자산이 없습니다.")
            return

        service = FundamentalAnalysisService(db)
        
        # 현재 연도 기준으로 최신 확정 재무제표는 보통 전년도입니다.
        current_year = datetime.now().year
        fiscal_year = current_year - 1 
        
        for symbol in symbols:
            try:
                # 1. 재무 데이터 수집 및 계산
                # DART API 사용량 제한에 주의해야 하므로 실제 운영시에는 time.sleep()이 필요할 수 있습니다.
                logger.info(f"[{symbol}] 펀더멘털 데이터 수집 시도...")
                service.calculate_and_save_fundamentals(ticker=symbol, fiscal_year=fiscal_year)
                
            except Exception as e:
                logger.error(f"[{symbol}] 펀더멘털 갱신 중 오류 발생: {e}")
                
        logger.info("--- [배치 작업] 펀더멘털 데이터 갱신 완료 ---")
    except Exception as e:
        logger.error(f"배치 작업 전체 오류: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # 매일 오후 4시 30분에 실행 (한국 주식시장 마감 15:30 이후)
        scheduler.add_job(
            update_fundamentals_job, 
            'cron', 
            hour=16, 
            minute=30, 
            id="daily_fundamentals_update", 
            replace_existing=True
        )
        scheduler.start()
        logger.info("백그라운드 스케줄러(APScheduler)가 시작되었습니다.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("백그라운드 스케줄러가 종료되었습니다.")
