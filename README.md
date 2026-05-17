# 📈 KIS Invest: AI 기반 하이브리드 투자 의사결정 플랫폼

> **일목균형표(Ichimoku Cloud) 기술적 지표**와 **기업 펀더멘털(S-RIM 가치평가) 분석**을 유기적으로 결합하고, **시장 국면 감지(Market Regime Detection)** 및 **켈리 공식(Kelly Criterion) 자금 관리**를 적용한 후 **Google Gemini AI 브리핑**을 제공하는 프리미엄 풀스택 투자 의사결정 보조 웹 애플리케이션입니다.

---

## 🌟 핵심 프리미엄 기능 (Key Features)

### 1. 📊 기술적 분석 엔진 (Technical Analysis Engine)
- **일목균형표 시그널 탐지**: 구름대 돌파, 쿠모 트위스트(Kumo Twist), 3역 호전 등 다차원 복합 기술적 시그널 실시간 연산.
- **다중 타임프레임 리샘플링**: 한국투자증권(KIS) API 분봉 데이터를 실시간 수집하여 4시간봉, 일봉 등 다양한 타임프레임으로 변환 및 분석.
- **실시간 데이터 스트리밍**: WebSocket (`ConnectionManager`) 기반 실시간 종목 가격 및 기술적 분석 지표 실시간 브로드캐스팅.

### 2. 🏢 펀더멘털 분석 및 가치평가 (Fundamental Valuation)
- **OpenDART 실시간 연동**: 금융감독원 DART API를 통해 상장 기업의 재무제표(매출액, 영업이익, 당기순이익, 자산/자본 총계 등)를 실시간 수집 및 캐싱.
- **S-RIM 적정 주가 엔진**: 한국시장 표준 초과이익 모형(S-RIM) 공식 기반으로 10년 초과이익 현재가치 및 회사채(BBB+) 금리 할인율을 반영한 적정 주가 연산.
- **Value-Trend 복합 스코어**: 펀더멘털 점수(70%)와 기술적 분석 점수(30%)를 결합하여 최종 추천 등급(`STRONG_BUY` / `BUY` / `HOLD` / `AVOID`) 분류.

### 3. 🎯 자산 배분 및 시장 국면 감지 (Portfolio & Capital Management)
- **시장 국면 감지 (Market Regime Detection)**: KOSPI/KOSDAQ 지수의 50일 및 200일 이동평균선(SMA) 정배열/역배열을 분석해 상승(BULL), 하락(BEAR), 횡보(SIDEWAYS) 국면 감지. 국면에 따라 기술적/펀더멘털 분석 가중치 동적 조절.
- **켈리 공식 기반 자금 관리 (Kelly Criterion Position Sizing)**: 개별 전략의 과거 백테스트 승률(Win Rate) 및 손익비(Win/Loss Ratio)를 연산하여 수학적으로 최적화된 포트폴리오 권장 투자 비중(Fractional Kelly) 도출.
- **실시간 Ledger 및 P&L**: 보유 종목 매수/매도 시 가중평균 매수단가(WAC) 자동 계산 엔진 및 실시간 평가 손익(P&L) 시각화.

### 4. 🤖 Google Gemini AI 투자 브리핑 (AI Investment Thesis)
- **개인 맞춤형 리포팅**: Google Gemini API (`gemini-1.5-flash` 모델)와 실시간 연동.
- **의사결정 논거 생성**: 감지된 시장 국면, 켈리 공식 비중, 백테스트 승률, S-RIM 펀더멘털 및 기술적 시그널을 종합 분석하여 트레이더 관점의 3단락 분량 '투자 논거(Investment Thesis)' 자동 생성.
- **대시보드 AI Insights**: 메인 대시보드 벤토 박스(Bento Box) 레이아웃에 탑재되어 직관적인 행동 가이드 제공.

### 5. 🧪 백테스팅 및 리포팅 엔진 (Stochastic Backtesting)
- **성능 메트릭 산출**: 과거 시계열 가격 데이터 기준 승률(Win Rate), Sharpe Ratio(위험 대비 수익률), 최대 낙폭(MDD), 벤치마크 대비 초과 수익률 등 시각화 리포트 제공.
- **인터랙티브 리포팅**: React 기반 동적 백테스트 차트 및 거래 내역 타임라인 추적.

### 6. 🔐 인증 및 보안 인프라 (Security & Infrastructure)
- **JWT 보안 인증**: OAuth2 규격 및 Bcrypt 패스워드 해싱을 통한 회원가입/로그인 라우터 지원.
- **Fernet API Key 암호화**: 사용자별 KIS API Key 및 Secret, OpenDART API Key를 PostgreSQL에 대칭 암호화(Fernet)하여 안전하게 보관.

---

## 📂 프로젝트 구조 (Project Directory)

```
KIS Invest/
├── backend/                  # 백엔드 (FastAPI & SQLAlchemy)
│   ├── app/
│   │   ├── api/             # API 공통 의존성 및 설정
│   │   ├── core/            # 핵심 분석 엔진 (Ichimoku 등)
│   │   ├── database/        # DB 연결 및 SQLAlchemy ORM 모델
│   │   ├── repositories/    # 데이터 액세스 레이어 (CRUD)
│   │   ├── routers/         # API 라우터 (signals, fundamentals, ai, backtest 등)
│   │   ├── schemas/         # Pydantic 데이터 검증 스키마
│   │   └── services/        # 핵심 비즈니스 로직 (AI, Portfolio, Backtest, DART 등)
│   ├── tests/               # Pytest 단위 테스트 코드
│   ├── alembic/             # 데이터베이스 마이그레이션 이력 관리
│   ├── alembic.ini          # Alembic 설정 파일
│   ├── requirements.txt     # Python 의존성 목록
│   └── .env                 # 환경 변수 설정 파일 (암호화 키, API 토큰)
├── frontend/                 # 프론트엔드 (React + TypeScript + TailwindCSS)
│   ├── src/
│   │   ├── api/             # 백엔드 API 클라이언트 (kis, ai 등)
│   │   ├── components/      # UI 컴포넌트 (Bento Box, Chart, AI Card, Skeleton 등)
│   │   ├── hooks/           # 커스텀 React 훅 (WebSocket 등)
│   │   ├── pages/           # 주요 뷰 (Dashboard, Portfolio, BacktestReport 등)
│   │   └── store/           # 전역 상태 관리 (Zustand 등)
│   ├── package.json         # Node.js 의존성 목록
│   └── tailwind.config.js   # TailwindCSS 테마 설정
├── checklist.md              # 프로젝트 개발 및 배포 체크리스트 (버전 관리)
└── README.md                 # 프로젝트 설명 파일
```

---

## 🛠️ 시작 가이드 (Getting Started)

### 1. 백엔드 설정 및 실행
Python 3.9 이상 가상환경 활성화 상태에서 진행합니다.

```bash
# 1. 의존성 패키지 설치
pip install -r backend/requirements.txt

# 2. .env 파일 생성 및 값 채우기 (backend/.env)
# KIS_API_KEY, KIS_API_SECRET, DART_API_KEY, GEMINI_API_KEY, ENCRYPTION_KEY 등 기입

# 3. 데이터베이스 최신 스키마 마이그레이션
alembic upgrade head

# 4. FastAPI 로컬 개발 서버 실행
uvicorn backend.app.main:app --reload --port 8000
```

### 2. 프론트엔드 설정 및 실행
Node.js 16 이상 환경이 필요합니다.

```bash
# 1. 프론트엔드 디렉터리 이동
cd frontend

# 2. npm 의존성 설치
npm install

# 3. 개발 서버 실행
npm start
```

---

## 🧪 테스트 실행 (Running Tests)

백엔드 핵심 기능들에 대해 총 **9개의 단위 테스트(Pytest)**가 구축되어 있습니다. 모든 테스트는 견고함과 예외 상황 대응 능력을 검증하며 100% 정상 통과합니다.

- **테스트 커버리지**: 일목균형표 계산 로직, S-RIM 주가 계산 모듈, 백테스트 성과 지표 산출, 켈리 기준 및 시장 국면 판단 엔진.

```bash
# PYTHONPATH 설정과 함께 pytest 실행 (루트 디렉터리에서 실행 권장)
$env:PYTHONPATH="backend"; .\.venv\Scripts\pytest
```

**테스트 결과 요약**:
```text
collected 9 items
backend/tests/test_backtest_service.py .                                 [ 11%]
backend/tests/test_ichimoku.py ..                                        [ 33%]
backend/tests/test_portfolio_management.py ....                          [ 77%]
backend/tests/test_srim.py ..                                            [100%]

======================== 9 passed, 1 warning in 4.44s =========================
```

---

## 🎨 프리미엄 UI/UX 디자인 가이드라인
- **Bento Box 레이아웃**: 모든 지표와 카드들이 현대적인 Bento Grid 형태로 배치되어 한눈에 고밀도 정보를 보기 쉽게 파악할 수 있습니다.
- **Glassmorphism**: 다크 모드 기반의 반투명 배경 및 그라데이션 블러 처리를 전반에 적용하여 우아하고 고급스러운 사용자 경험을 극대화했습니다.
- **Skeleton UI & Dynamic Fetching**: 화면 로딩 시 레이아웃 팅김 현상을 방지하는 스켈레톤 애니메이션과 다이나믹 비동기 로딩을 도입해 속도감을 개선했습니다.
