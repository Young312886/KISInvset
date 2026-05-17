# KIS Invest: 프로젝트 개발 및 배포 체크리스트

이 문서는 '일목균형표 기반 기술적 분석'에 '기업 펀더멘털 분석'을 결합한 **종합 투자 의사결정 보조 웹 애플리케이션** 프로젝트의 개발 및 고도화를 위한 체크리스트입니다.

## 📊 프로젝트 현재 상태 분석 (2026-05-17)

- **백엔드**: FastAPI 기반 구조화 완료. KIS API 연동(병렬 처리 최적화) 및 일목균형표 연산 구현. **켈리 공식 기반 포트폴리오 비중 조절**, **50일/200일 이평선 기반 시장 국면 감지**, **Google Gemini API 기반 AI 투자 브리핑 시스템 구축 완료**.
- **인증/보안**: JWT 기반 인증 및 **Fernet 기반 API 키 암호화 저장 완료**.
- **펀더멘털**: DART 연동 서비스, S-RIM 가치평가, Value-Trend 스코어링 엔진 완료.
- **프론트엔드**: React + Tailwind 대시보드 고도화 완료. **비동기 데이터 로딩 및 Skeleton UI 적용**, **AI Insights 벤토 박스 대시보드 카드 연동 완료**.
- **품질 관리**: Pytest 기반으로 S-RIM, 일목균형표, 백테스트 엔진, 포트폴리오 관리 핵심 모듈 단위 테스트 100% 통과 검증 완료.
- **향후 핵심 목표**: 모의투자 연동 테스트 환경 구축 및 안정적인 프로덕션 배포 파이프라인 마무리.

---

## ✅ 1. 인프라 및 기반 설정 (Infrastructure & DB)

- [x] **`.env` 환경 변수 구조 확장**
  - [x] KIS API Key, Secret 설정 (`.env.example` 업데이트)
  - [x] **[NEW]** Open DART API Key 발급 필드 추가 (`DART_API_KEY`)
  - [x] JWT 인증 관련 설정 추가 (`JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
  - [x] API Key 암호화용 Fernet Key 설정 추가 (`ENCRYPTION_KEY`)
  - [x] `.env` 실제 값 채우기 (KIS, DART 발급 필요)
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
  - [x] 최초 마이그레이션 파일 생성 (`alembic revision --autogenerate -m "initial_schema"`)
  - [x] DB에 실제 적용 (`alembic upgrade head`)
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
- [x] **실시간 시세 조회 성능 최적화**
  - [x] `ThreadPoolExecutor` 기반 다중 종목 현재가 병렬 페칭 구현
  - [x] KIS API `custtype: P` 헤더 및 지수 조회 파라미터 보정
- [x] **실시간 WebSocket 서비스**
  - [x] 백엔드 시세 수신 및 프론트엔드 브로드캐스팅 (`ConnectionManager`, `MarketStreamService` 구현)

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
  - [x] **[NEW]** shadcn/ui 기반 컴포넌트 모듈화 (Button, Card, Badge, Table 등)
- [x] **종목 Snapshot 대시보드 구현**
  - [x] 일목균형표 인터랙티브 차트 고도화 (구름대 시각화 완벽 대응)
  - [x] **재무 건강도 레이더 차트** 추가 (수익성, 성장성, 안전성, 활동성, 배당 매력도)
  - [x] 기술적 시그널과 재무 스코어의 통합 결과 UI (Value-Trend 점수 표시)
- [x] **메인 대시보드 고도화**
  - [x] KPI 카드 (시장 지수 및 자산 현황)
  - [x] 실시간 시그널 패널 및 Market Pulse (심리 지수)
  - [x] 포트폴리오 자산 비중 시각화 (Portfolio Allocation)
  - [x] **[NEW]** 대시보드 비동기 로딩 및 병렬 페칭 (무한 로딩 해결)
- [x] **성능 최적화 및 UI 폴리싱 (UI/UX Polish)**
  - [x] **[NEW]** 대시보드 Skeleton UI 적용 (사용자 경험 개선)
  - [x] **[NEW]** 종목 Snapshot 페이지 동적 데이터 바인딩 및 전역 로딩 제거
- [x] **포트폴리오(Ledger) 및 자산 관리 뷰**
  - [x] 실시간 평가 손익 및 자산 비중 시각화 (`Portfolio.tsx`)
  - [x] 보유 종목 상세 리스트 (수량, 평단가, 수익률 등)
  - [x] 거래 내역(History) 타임라인 뷰

## 🚀 5. 자산 관리 로직 및 배포 (Production)

- [x] **자산 관리 (Ledger System) 정밀화**
  - [x] **[NEW]** 매수/매도 시 평단가(WAC) 자동 계산 엔진 구현
  - [x] **[NEW]** 실시간 평가 손익(P&L) 산출 API 개발
  - [x] **[NEW]** KIS API 연동 실제 주문(Order) 기능 구현 (시장가/지정가)
  - [x] **[NEW]** 계좌 예수금(Cash) 추적 및 통합 관리 로직
- [x] **백테스트 엔진 (Backtesting Engine) [NEW]**
  - [x] 과거 OHLCV 기반 전략 시뮬레이션 환경 구축 (`BacktestService`)
  - [x] 백테스팅 API 엔드포인트 개설 (`/backtest/run`)
  - [x] **[NEW]** 시각화 리포트 및 결과 대시보드 구축 (`BacktestReport.tsx`)
- [x] **고도화된 포트폴리오 관리 및 AI 브리핑 시스템 [NEW]**
  - [x] **시장 국면 감지 엔진 (Market Regime Detection)**: 50일/200일 이평선(SMA) 기반 BULL/BEAR/SIDEWAYS 감지 및 가중치 동적 산출 구현 (`PortfolioManagementService`)
  - [x] **켈리 공식 기반 자금 관리 (Kelly Criterion Position Sizing)**: 백테스트 승률/손익비 기반 Fractional Kelly 권장 투자 비중 연산 구현 (`PortfolioManagementService`)
  - [x] **Google Gemini AI 브리핑 시스템**: `gemini-1.5-flash` 모델 기반 시장 국면, 켈리 비중, 백테스트 승률, 펀더멘털 점수 통합 투자 논거(Briefing) 생성 API 구현 (`AIService`, `/ai/briefing/{symbol}`)
  - [x] **프론트엔드 AI Insights 대시보드 연동**: 대시보드 Bento Box 레이아웃 내 AI 브리핑 카드 및 권장 비중/시장 국면 시각화 구현 (`AIBriefingCard.tsx`, `ai.ts`)
  - [x] **포트폴리오 평가 손익(P&L) 정보 보강**: 보유 자산 리스트에 평가 손익액 및 수익률 정보 추가 (`kis.ts`, `Portfolio.tsx`)
  - [x] **신규 백테스팅 및 포트폴리오 관리 검증용 Pytest 작성**: `test_backtest_service.py`, `test_portfolio_management.py` 추가 및 테스트 100% 통과 완료 (`pytest`)
- [ ] **테스트 및 CI/CD 환경 구축**
  - [x] 핵심 분석 로직(S-RIM, 일목균형표)에 대한 Pytest 작성
  - [x] GCP Cloud Run / Vercel 기반 CI/CD 환경 구축 및 스테이징 배포
  - [ ] DART API Key 실제 발급 후 연동 테스트
  - [ ] 실제 주문/매수/매도 로직 모의투자 테스트 및 안정성 확보(Roadmap)

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
