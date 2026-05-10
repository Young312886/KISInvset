# KIS Invest: 프로젝트 개발 및 배포 체크리스트

이 문서는 '일목균형표 기반 기술적 분석'에 '기업 펀더멘털 분석'을 결합한 **종합 투자 의사결정 보조 웹 애플리케이션** 프로젝트의 개발 및 고도화를 위한 체크리스트입니다.

## 📊 프로젝트 현재 상태 분석 (2026-05-06)
- **백엔드**: FastAPI 기반 구조화 완료. KIS API 연동 및 일목균형표 기초 연산 구현. PostgreSQL 모델링(사용자, 자산, 거래, 시그널, 펀더멘털) 완료.
- **인증**: JWT 기반 회원가입/로그인/토큰 검증 시스템 **완료** (bcrypt 해싱, Bearer 토큰, `/auth/register`, `/auth/login`, `/auth/me` 엔드포인트).
- **펀더멘털**: DART 연동 서비스, S-RIM 가치평가, Value-Trend 스코어링 엔진 **코드 완료** (DART API Key 발급 후 실사용 가능).
- **프론트엔드**: React + Tailwind 대시보드 기초 구현. Lightweight-charts 연동 완료.
- **향후 핵심 목표**: 기술적 분석(차트)에 펀더멘털 분석(재무/가치평가)을 결합하여, **"무엇을(종목 선정)"**과 **"언제(타이밍)"**를 동시에 해결하는 서비스형 포트폴리오로 진화.

---

## ✅ 1. 인프라 및 기반 설정 (Infrastructure & DB)
- [x] **`.env` 환경 변수 구조 확장**
  - [x] KIS API Key, Secret 설정 (`.env.example` 업데이트)
  - [x] **[NEW]** Open DART API Key 발급 필드 추가 (`DART_API_KEY`)
  - [x] JWT 인증 관련 설정 추가 (`JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
  - [x] API Key 암호화용 Fernet Key 설정 추가 (`ENCRYPTION_KEY`)
  - [ ] `.env` 실제 값 채우기 (KIS, DART 발급 필요)
- [x] **`requirements.txt` 의존성 확장**
  - [x] `alembic` (DB 마이그레이션)
  - [x] `OpenDartReader` (재무 데이터)
  - [x] `python-jose`, `passlib`, `python-multipart` (JWT 인증)
  - [x] `cryptography` (API Key 암호화)
  - [ ] 실제 `pip install -r requirements.txt` 실행
- [x] **Alembic 마이그레이션 도구 설정** 
  - [x] `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako` 생성
  - [x] `env.py`에서 `.env`의 `DATABASE_URL` 자동 주입 연동
  - [x] `ALEMBIC_GUIDE.md` 문서 작성
  - [ ] 최초 마이그레이션 파일 생성 (`alembic revision --autogenerate -m "initial_schema"`)
  - [ ] DB에 실제 적용 (`alembic upgrade head`)
- [x] **데이터베이스 모델 전면 확장** (`app/database/models.py`)
  - [x] `User` 모델 보강 (`is_active`, `updated_at`, `watchlist` 관계)
  - [x] `KisAccount` 모델 보강 (`account_type`, 관계 정리)
  - [x] `Asset` 모델 보강 (`company_name`, `UniqueConstraint`)
  - [x] `TradeHistory` 모델 보강 (`commission`, `tax`, `memo`)
  - [x] `WatchlistItem` 모델 신규 추가
  - [x] `OhlcvData` 모델 보강 (`UniqueConstraint` 추가)
  - [x] **[NEW]** `CompanyFundamentals` 테이블 추가 (수익성/가치/성장성/안전성/배당/S-RIM 전 지표)
  - [x] **[NEW]** `ValueTrendScore` 테이블 추가 (복합 점수 결과)
- [x] **사용자 인증 시스템 (Auth)** ✅ 완료
  - [x] JWT 기반 로그인/회원가입 라우터 (`/auth`) 구현
    - [x] `POST /auth/register` — 회원가입 (이메일·사용자명 중복 확인, bcrypt 해싱)
    - [x] `POST /auth/login` — 로그인 JSON (JWT Access Token 발급)
    - [x] `POST /auth/token` — Swagger UI OAuth2 form-data 로그인
    - [x] `GET /auth/me` — 현재 로그인 사용자 정보 조회
  - [x] `get_current_user` Dependency 구현 및 각 라우터에 적용 (`app/api/dependencies.py`)
  - [x] Fernet 암호화를 이용한 실제 API Key 암호화/복호화 구현 (`encrypt_api_key`, `decrypt_api_key`)

## ⚙️ 2. 기술적 분석 엔진 (Technical Analysis - Backend)
- [x] **데이터 리샘플링 엔진**
  - [x] KIS 분봉 데이터를 활용한 다중 타임프레임(4시간봉 등) 생성 로직
- [x] **일목균형표 시그널 로직 고도화**
  - [x] 구름대 돌파, 쿠모 트위스트, 3역 호전 등 복합 시그널 탐지
- [ ] **실시간 WebSocket 서비스**
  - [ ] 백엔드 시세 수신 및 프론트엔드 브로드캐스팅

## 🏢 3. 펀더멘털 분석 엔진 (Fundamental Analysis - Backend)
- [x] **스키마, 리포지토리 기반 코드 구축**
  - [x] `fundamental_schema.py`: `FundamentalsResponse`, `ValueTrendScoreResponse`, `ScreeningRequest` 스키마 정의
  - [x] `fundamental_repository.py`: `FundamentalsRepository` (upsert/조회/스크리닝), `ValueTrendScoreRepository` 구현
- [x] **`DartService`: OpenDART 연동 서비스 구현** (`app/services/fundamental_service.py`)
  - [x] `OpenDartReader` 클라이언트 Lazy 초기화 및 에러 처리
  - [x] 연결/개별 재무제표 자동 전환 로직
  - [x] 매출액, 영업이익, 순이익, 총자산/자본/부채 수집
  - [ ] 실제 DART API Key 발급 및 `.env` 설정 후 테스트
- [x] **`SRimService`: S-RIM 적정 주가 계산 엔진 구현**
  - [x] 10년 초과이익 현재가치 합산 로직 (표준 공식 구현)
  - [x] 할인율(BBB+ 회사채 수익률 기본값 4.5%) 적용
- [x] **`FundamentalAnalysisService`: 통합 분석 서비스 구현**
  - [x] DART 수집 → 지표 계산 → S-RIM → DB 저장 파이프라인
  - [x] 수익성(ROE, ROA, 영업이익률), 성장성(YoY), 안전성(부채비율) 지표 계산
- [x] **`ScoringService`: Value-Trend 복합 스코어링 엔진 구현**
  - [x] 5개 영역(수익성/가치/성장성/안전성/배당) 개별 점수화 (0~100점)
  - [x] 펀더멘털 70% + 기술적 시그널 30% 가중 종합 점수 산출
  - [x] 추천 등급 자동 분류 (`STRONG_BUY`/`BUY`/`HOLD`/`AVOID`)
- [x] **`/fundamentals` 라우터 추가** (`app/routers/fundamentals.py`)
  - [x] `POST /{ticker}/collect`: DART 데이터 수집 및 저장
  - [x] `GET /{ticker}`: 특정 종목 재무 데이터 조회
  - [x] `GET /`: 전체 종목 목록 (시장 필터)
  - [x] `POST /screen`: 퀀트 멀티 팩터 스크리닝
  - [x] `GET /{ticker}/score`: Value-Trend 점수 조회
  - [x] `POST /{ticker}/score/calculate`: 점수 계산 및 저장
- [x] **`/fundamentals` 라우터를 `main.py`에 등록** → ✅ 완료
- [x] **배치(Batch) 스케줄러 구현** (APScheduler 활용)
  - [x] 전체 관심 종목 일괄 데이터 갱신 (매일 장 마감 후 자동 실행)

## 🎨 4. 프론트엔드 UI/UX 고도화 (Frontend)
- [x] **디자인 시스템 및 레이아웃 (Premium Aesthetics)**
  - [x] 다크/라이트 모드, Glassmorphism, Bento Box 레이아웃 적용
- [x] **종목 Snapshot 대시보드 구현 [NEW]**
  - [x] 일목균형표 인터랙티브 차트 고도화 (구름대 시각화 완벽 대응)
  - [ ] **재무 건강도 레이더 차트** 추가 (수익성, 성장성, 안전성, 활동성, 배당 매력도)
  - [ ] 기술적 시그널과 재무 스코어의 통합 결과 UI (Value-Trend 점수 표시)
- [ ] **포트폴리오(Ledger) 관리 뷰**
  - [ ] 실시간 평가 손익 및 자산 비중 시각화

## 🚀 5. 자산 관리 로직 및 배포 (Production)
- [ ] **자산 관리 (Ledger System) 정밀화**
  - [ ] 매수/매도 평균 단가 계산 및 수수료/세금 반영 로직
- [ ] **테스트 및 CI/CD 환경 구축**
  - [ ] 핵심 분석 로직(S-RIM, 일목)에 대한 Pytest 작성
  - [ ] GitHub Actions (백엔드 GCP Cloud Run 배포)
  - [ ] Vercel (프론트엔드 배포)

---

## 📅 단계별 확장 로드맵 (Roadmap)

### Phase 1: 기반 인프라 및 기술적 분석 고도화 (Week 1~2)
- **목표**: 안전한 회원 체계, KIS API 완벽 연동, 정교한 차트 데이터 확보
- JWT 인증, DB 세팅, 4시간봉 리샘플링, 복합 일목균형표 시그널 백엔드 구현

### Phase 2: 펀더멘털 데이터 파이프라인 및 가치 평가 (Week 3~4) **[Focus]**
- **목표**: "무엇을 살 것인가"에 대한 데이터베이스 구축
- OpenDART API 연동, `company_fundamentals` DB 갱신 배치 생성, S-RIM 적정 주가 연산 서비스 개발

### Phase 3: 통합 스코어링 및 프론트엔드 대시보드 (Week 5~6) **[Focus]**
- **목표**: 사용자에게 직관적이고 강력한 인사이트 제공
- **Value-Trend 스코어링 시스템** 개발 (재무+차트 교집합 스크리닝).
- **재무 건강도 레이더 차트** 및 Premium UI/UX 디자인 전면 적용.

### Phase 4: 자산 관리(Ledger) 정밀화 및 상용 배포 (Week 7~8)
- **목표**: 실제 자산 추적 기능 완성 및 안정적인 서비스 론칭
- 실시간 평가 손익 계산, 포트폴리오 관리 뷰 완성, CI/CD 구축, 최종 테스트 및 배포

