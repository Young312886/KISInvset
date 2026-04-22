from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# DATABASE_URL은 settings에서 통합 관리
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    # PostgreSQL 연결 풀 설정
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # 연결 유효성 사전 확인
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI Dependency: 요청마다 DB 세션을 생성하고 사용 후 닫습니다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
