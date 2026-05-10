# KIS Invest - 프론트엔드 상세 개발 내역서 (Phase 3)

## 1. 개요 및 핵심 목표 (Overview & Core Goals)
KIS Invest의 프론트엔드는 단순한 정보 나열을 넘어, 사용자에게 **"전문적이면서도 직관적인 투자 인사이트"**를 제공하는 것을 목표로 합니다.
백엔드에서 완성된 '일목균형표(기술적 분석)'와 'S-RIM 및 Value-Trend(펀더멘털 분석)' 데이터를 시각적으로 극대화하여 표현해야 합니다.

*   **Premium Aesthetics**: 단순 텍스트/표 형태를 탈피. Dark/Light 모드 지원, Glassmorphism(반투명/블러 효과) 적용, 정보 위계를 위한 Bento Box 형태의 그리드 레이아웃 적용.
*   **Data Visualization**: Lightweight-charts를 활용한 매끄러운 캔들 및 일목 구름대 차트, Recharts(또는 Chart.js)를 활용한 재무 건강도 레이더 차트 및 자산 비중 파이 차트 구현.
*   **Responsive & Smooth**: 다양한 디바이스(PC, 태블릿) 대응 및 컴포넌트 간 전환 시 부드러운 마이크로 애니메이션 적용.

---

## 2. 기술 스택 및 주요 라이브러리 (Tech Stack)
*   **Framework**: `React` (또는 Next.js App Router - 프로젝트 설정에 따라 택 1, 현재 React SPA로 가정)
*   **Styling**: `Tailwind CSS` (유틸리티 클래스로 빠른 스타일링), `framer-motion` (애니메이션 및 부드러운 화면 전환)
*   **State Management**: `Zustand` (가볍고 직관적인 전역 상태 관리 - 유저 세션, 다크모드, 선택된 종목 등)
*   **Data Fetching**: `React Query` (서버 상태 관리, 캐싱, API 로딩/에러 처리)
*   **Charting**:
    *   `lightweight-charts` (TradingView 기반): OHLCV 캔들스틱 및 일목균형표(전환선, 기준선, 후행스팬, 구름대 영역 채우기) 구현.
    *   `recharts`: 레이더 차트(재무 건강도) 및 파이/도넛 차트(포트폴리오 비중) 구현.
*   **Routing**: `react-router-dom`

---

## 3. 핵심 화면 명세 (Core Screens Specification)

### 3.1. 공통 레이아웃 (Layout & Design System)
*   **Sidebar (GNB)**: 대시보드, 관심 종목, 포트폴리오, 설정(다크모드 토글, 로그아웃) 메뉴.
*   **Top Header**: 검색 바(종목 검색), 현재 사용자 프로필 및 알림.
*   **디자인 테마**:
    *   Background: 어두운 회색/블랙 (다크모드 기준)
    *   Card (Bento Box): 반투명한 흰색/회색 (가우시안 블러 `backdrop-blur-md` 적용) + 은은한 테두리(`border-white/10`).
    *   Point Colors: 상승(Red/Pink 계열), 하락(Blue/Teal 계열) - 한국 주식 시장 기준 색상 반영.

### 3.2. 대시보드 홈 (Dashboard Home)
*   **Market Overview**: 코스피/코스닥 주요 지수 요약 카드.
*   **Watchlist 퀵 뷰**: 관심 종목의 현재가, 당일 등락률, 그리고 백엔드에서 판정한 **Value-Trend 스코어 기반 추천 등급(STRONG BUY 등)**을 리스트/카드 형태로 노출.
*   **최근 시그널 알림**: 일목균형표 3역 호전 등 기술적 돌파가 일어난 종목을 실시간/최근 순으로 알림 패널에 표시.

### 3.3. 종목 스냅샷 뷰 (Stock Snapshot - 가장 중요 ⭐)
특정 종목(예: 삼성전자)을 클릭했을 때 나타나는 상세 화면입니다. Bento Box 그리드로 3가지 핵심 패널을 배치합니다.

1.  **헤더 패널 (상단)**
    *   종목명, 티커, 현재가, 전일 대비 등락률.
    *   **Value-Trend 통합 점수 (원형 프로그레스 바)**: 예) 85점. 중앙에 크게 배치.
    *   **투자의견 뱃지**: `STRONG BUY`, `BUY`, `HOLD`, `AVOID` 중 하나를 색상이 들어간 뱃지로 표시.

2.  **기술적 분석 패널 (중앙 좌측 - 가장 큰 영역)**
    *   **일목균형표 차트**: `lightweight-charts` 사용.
    *   캔들 차트 위에 전환선/기준선 렌더링.
    *   선행스팬1, 선행스팬2를 그리고 그 사이 공간을 색칠(양운은 옅은 붉은색, 음운은 옅은 푸른색)하여 **구름대**를 직관적으로 시각화.
    *   우측 상단에 타임프레임(15분, 1시간, 4시간, 일봉) 선택 탭 배치.

3.  **펀더멘털 분석 패널 (중앙 우측)**
    *   **재무 건강도 레이더 차트 (`recharts`)**: 수익성, 가치(S-RIM 밸류에이션), 성장성, 안전성, 배당 매력도의 5축 레이더 차트.
    *   **S-RIM 요약**: 현재 주가 vs S-RIM 적정 주가 막대 그래프 비교 (저평가/고평가 직관적 확인).
    *   주요 지표 요약 수치: ROE, 부채비율, 영업이익률 등.

### 3.4. 포트폴리오(Ledger) 뷰 (Portfolio View)
*   **자산 요약 카드**: 총 자산, 매입 금액, 평가 금액, 총 평가 손익(%, 원화).
*   **자산 비중 차트**: 도넛 차트로 섹터별 또는 종목별 보유 비중 시각화.
*   **보유 종목 리스트 (Table)**:
    *   컬럼: 종목명, 보유 수량, 매수 평균가, 현재가, 수익률, 해당 종목의 현재 Value-Trend 점수.
    *   수익률에 따라 글자 색상 동적 변경.

---

## 4. API 연동 및 상태 관리 계획 (Integration Plan)

| 기능 분류 | Endpoint (Backend) | 역할 및 상태 관리 로직 |
| :--- | :--- | :--- |
| **Auth** | `/auth/login`, `/auth/me` | 로그인 성공 시 `Zustand` 스토어에 JWT 저장 및 전역 `User` 상태 업데이트. API 요청 시 헤더에 Bearer 토큰 주입. |
| **Search/List** | `/fundamentals/` | 종목 리스트 검색 및 자동완성. `React Query`로 캐싱. |
| **Technical** | `/signals/ichimoku/{symbol}` | 선택된 타임프레임에 맞춰 일목균형표 데이터를 불러와 차트 컴포넌트에 주입 (`useQuery`). |
| **Fundamental** | `/fundamentals/{ticker}/score` | 해당 종목의 레이더 차트 데이터 및 Value-Trend 점수 로드. |
| **Portfolio** | `/assets/portfolio` | 보유 자산 목록 및 평균 단가 데이터를 불러와 포트폴리오 뷰에 바인딩. |

---

## 5. 단계별 개발 순서 (Development Steps)

1.  **Step 1: 환경 구성 및 라우팅 설정**
    *   React(또는 Vite) 프로젝트 생성 및 Tailwind CSS 설정.
    *   글로벌 CSS(`index.css`)에 다크모드 및 Glassmorphism 유틸리티 클래스 정의.
    *   React Router로 기본 페이지 골격 구축.
2.  **Step 2: API 클라이언트 및 인증 상태 연동**
    *   Axios 인스턴스 생성 (인터셉터로 토큰 주입).
    *   Zustand를 이용한 로그인 상태 관리 및 보호된 라우트(Protected Route) 구현.
3.  **Step 3: 디자인 시스템 & 공통 컴포넌트 제작**
    *   Sidebar, Header, BentoCard, Badge, Spinner 등 재사용 가능한 UI 요소 제작.
4.  **Step 4: 종목 스냅샷 화면 구현 (핵심)**
    *   레이더 차트 컴포넌트(Recharts) 구현.
    *   일목균형표 차트 컴포넌트(Lightweight-charts) 고도화 (구름대 색칠 알고리즘 포함).
5.  **Step 5: 대시보드 및 포트폴리오 연동**
    *   남은 화면 구현 및 백엔드 API와의 최종 데이터 바인딩.
    *   애니메이션(`framer-motion`) 추가 및 반응형 레이아웃 폴리싱.
