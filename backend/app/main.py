from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.connection import Base, engine
from .routers import signals, assets, fundamentals, auth, watchlist, trade_history, market, backtest

# NOTE: Alembic을 도입한 이후로는 아래 create_all을 사용하지 않습니다.
# 개발 초기 편의를 위해 남겨두었으나, 운영 환경에서는 반드시 주석 처리하세요.
# 대신 'alembic upgrade head' 명령어로 테이블을 생성/관리합니다.
# Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager
from .core.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()

app = FastAPI(
    title="KIS Invest Assistant API",
    description=(
        "한국투자증권(KIS) Open API와 DART 재무 데이터를 결합한 "
        "종합 투자 의사결정 보조 시스템. "
        "일목균형표 기술적 분석과 기업 펀더멘털 분석(Value-Trend 스코어링)을 제공합니다."
    ),
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- CORS 설정 ---
origins = [
    "http://localhost:3000",  # React 개발 서버
    # 배포 후 프론트엔드 URL 추가 (예: "https://your-app.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 헬스 체크 ---
@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "KIS Invest Assistant API v0.2.0",
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# --- 라우터 등록 ---
app.include_router(signals.router, prefix="/signals", tags=["📈 기술적 분석 (Ichimoku)"])
app.include_router(assets.router, prefix="/assets", tags=["💼 자산 관리 (Portfolio)"])
app.include_router(fundamentals.router, prefix="/fundamentals", tags=["🏢 펀더멘털 분석 (DART)"])
app.include_router(watchlist.router, prefix="/watchlist", tags=["⭐ 관심 종목 (Watchlist)"])
app.include_router(trade_history.router, prefix="/trade-history", tags=["🧾 매매 기록 (Ledger)"])
app.include_router(market.router, prefix="/market", tags=["📊 시장 데이터 (Market)"])
app.include_router(backtest.router, prefix="/backtest", tags=["🧪 전략 백테스트 (Backtest)"])

app.include_router(auth.router, prefix="/auth", tags=["🔐 Auth"])
