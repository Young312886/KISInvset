# PRD: Ichimoku Cloud Investment Assistant (K-Trading Bot)

## 1. 프로젝트 개요

한국투자증권(KIS) Open API를 활용하여 일목균형표 기반의 기술적 분석 시그널을 제공하고, 사용자의 투자 포트폴리오를 실시간으로 관리하는 웹 애플리케이션.

## 2. 주요 목표

- **기술적 지표 자동화**: 4시간봉 및 일봉 기준 일목균형표를 자동 계산하여 추세 분석.
- **실시간 데이터 처리**: KIS WebSocket을 통한 실시간 시세 수신 및 시그널 매칭.
- **자산 관리 시스템**: 개인 투자 자산(ISA/IRP 등)의 수익률 및 절세 현황을 정밀하게 추적하는 DB 기반 시스템 구축.

## 3. 기능적 요구사항

### 3.1. API 및 인증 관리

- KIS Developers OAuth 2.0 연동 (접근 토큰 발급 및 자동 갱신).
- 실시간 시세 및 체결 내역 수신을 위한 WebSocket 연결.

### 3.2. 분석 엔진 (Ichimoku Engine)

- **데이터 수집**: 국내/해외 주식 및 ETF의 OHLCV 데이터(4시간봉, 일봉) 수집.
- **지표 연산**: 전환선, 기준선, 선행스팬 1/2, 후행스팬 계산 로직 구현.
- **시그널 탐지**:
  - 주가가 구름대를 상향 돌파하는 시점 포착.
  - 전환선/기준선 골든크로스 및 추세 정배열 확인.

### 3.3. 포트폴리오 관리 (Ledger System)

- **거래 이력 관리**: 매수/매도 이력을 Header와 상세 Item 구조로 관리하여 데이터 정합성 유지.
- **수익률 계산**: 실시간 시세를 반영한 종목별/전체 자산 수익률 산출.
- **투자 리포트**: 기간별 투자 성과 및 세금/수수료를 반영한 실질 수익 확인.

## 4. 기술 스택 (Tech Stack)

- **Language**: Python 3.9+, TypeScript.
- **Backend**: FastAPI.
- **Frontend**: React (with Tailwind CSS).
- **Database**: PostgreSQL.
- **Libraries**:
  - `pandas`: 지표 계산 및 데이터 핸들링.
  - `requests`: REST API 통신.
  - `websocket-client`: 실시간 데이터 수신.
  - `lightweight-charts`: 주식 차트 시각화.

## 5. 데이터베이스 설계 방향

- `trade_orders`: 매매 주문 및 체결 내역 이력.
- `portfolio_assets`: 현재 보유 중인 자산 및 평단가 정보.
- `market_data_cache`: 지표 연산을 위한 최신 봉 데이터 캐싱.
- `user_settings`: 알림 설정 및 관심 종목 리스트.

## 6. 개발 로드맵

1. **Phase 1**: KIS API 연동 환경 구축 및 인증 모듈 개발.
2. **Phase 2**: 일목균형표 계산 알고리즘 및 백엔드 API 개발.
3. **Phase 3**: 데이터베이스 연동 및 자산 관리 로직 구현.
4. **Phase 4**: React 기반 프론트엔드 대시보드 및 차트 구현.