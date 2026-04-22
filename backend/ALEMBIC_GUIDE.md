# Alembic 마이그레이션 사용 가이드

이 문서는 KIS Invest 프로젝트의 데이터베이스 마이그레이션 관리 방법을 설명합니다.

## 사전 조건

`backend/.env` 파일에 `DATABASE_URL`이 올바르게 설정되어 있어야 합니다.

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/kis_invest
```

## 기본 명령어 (backend 폴더에서 실행)

```bash
# 현재 마이그레이션 상태 확인
alembic current

# 새 모델 변경사항을 감지하여 마이그레이션 파일 자동 생성
alembic revision --autogenerate -m "마이그레이션 설명 (예: add_company_fundamentals_table)"

# 최신 버전으로 DB 업그레이드 (실제 테이블 생성/변경)
alembic upgrade head

# 특정 버전으로 업그레이드
alembic upgrade <revision_id>

# 이전 버전으로 롤백
alembic downgrade -1

# 마이그레이션 히스토리 확인
alembic history --verbose
```

## 최초 설정 순서

```bash
# 1. backend 폴더로 이동
cd backend

# 2. 가상환경 활성화
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 첫 번째 마이그레이션 파일 생성 (전체 테이블 초기화)
alembic revision --autogenerate -m "initial_schema_with_fundamentals"

# 5. DB에 적용
alembic upgrade head
```

## 새 모델 추가 시 워크플로우

1. `app/database/models.py`에 새 모델(테이블) 추가
2. `alembic revision --autogenerate -m "add_new_table"` 실행
3. 생성된 파일을 `alembic/versions/`에서 검토
4. `alembic upgrade head`로 DB에 적용

## 주의사항

- `main.py`의 `Base.metadata.create_all(bind=engine)` 코드는 개발 편의용이며,
  Alembic 도입 후에는 **주석 처리**하고 `alembic upgrade head`를 사용하세요.
- `alembic/versions/` 폴더의 마이그레이션 파일은 **Git에 반드시 커밋**하세요.
