"""
Alembic 마이그레이션 환경 설정.

이 파일은 Alembic CLI 명령어 실행 시 호출됩니다.
SQLAlchemy 모델과 연동하여 자동으로 마이그레이션 스크립트를 생성하거나 실행합니다.
"""
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- 프로젝트 경로 설정 ---
# backend 폴더를 Python 경로에 추가하여 app 모듈을 import할 수 있게 합니다.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 프로젝트 설정 및 모델 import ---
from app.core.config import settings
from app.database.connection import Base
# 모든 모델을 import해야 Alembic이 변경을 감지할 수 있습니다.
import app.database.models  # noqa: F401 - 사이드 이펙트 임포트

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 핵심: .env의 DATABASE_URL을 Alembic에 주입 ---
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# --- 자동 마이그레이션을 위한 메타데이터 설정 ---
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    오프라인 모드로 마이그레이션 실행 (실제 DB 연결 없이 SQL 스크립트 생성).
    Usage: alembic upgrade --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    온라인 모드로 마이그레이션 실행 (실제 DB에 직접 적용).
    Usage: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # 컬럼 타입 변경도 감지하도록 설정
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
