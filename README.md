# KIS Invest

KIS Invest는 투자 분석 및 관리 도구로, 백엔드와 프론트엔드로 구성된 풀스택 애플리케이션입니다. 이 프로젝트는 투자 신호 분석, 자산 관리, 그리고 사용자 대시보드를 제공합니다.

## 프로젝트 구조

```
KIS Invest/
├── backend/                # 백엔드 코드
│   ├── .env               # 환경 변수 파일
│   ├── requirements.txt   # Python 의존성 목록
│   └── app/
│       ├── main.py        # 애플리케이션 진입점
│       ├── api/           # API 엔드포인트
│       ├── core/          # 핵심 로직 및 분석 모듈
│       ├── database/      # 데이터베이스 연결 및 모델
│       ├── repositories/  # 데이터 접근 레이어
│       ├── routers/       # 라우터 정의
│       ├── schemas/       # 데이터 스키마 정의
│       └── services/      # 비즈니스 로직
├── frontend/               # 프론트엔드 코드
│   ├── package.json       # Node.js 의존성 목록
│   ├── public/            # 정적 파일
│   └── src/               # React 소스 코드
│       ├── api/           # API 호출 로직
│       ├── components/    # 재사용 가능한 컴포넌트
│       └── pages/         # 페이지 컴포넌트
└── README.md               # 프로젝트 설명 파일
```

## 백엔드

백엔드는 Python과 FastAPI를 사용하여 구축되었습니다. 주요 기능은 다음과 같습니다:

- **API 엔드포인트**: `app/api/kis_api.py`
- **데이터베이스 연결**: `app/database/connection.py`
- **분석 모듈**: `app/core/analysis/ichimoku.py`

### 설치 및 실행

1. Python 3.9 이상이 설치되어 있는지 확인하세요.
2. 의존성 설치:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. 애플리케이션 실행:
   ```bash
   uvicorn app.main:app --reload
   ```

## 프론트엔드

프론트엔드는 React와 TypeScript를 사용하여 구축되었습니다. 주요 기능은 다음과 같습니다:

- **대시보드 페이지**: `src/pages/Dashboard.tsx`
- **Ichimoku 차트 컴포넌트**: `src/components/IchimokuChart.tsx`

### 설치 및 실행

1. Node.js 16 이상이 설치되어 있는지 확인하세요.
2. 의존성 설치:
   ```bash
   cd frontend
   npm install
   ```
3. 애플리케이션 실행:
   ```bash
   npm start
   ```

## 환경 변수

`.env` 파일을 사용하여 환경 변수를 설정합니다. 예제 파일은 `.env.example`에 제공됩니다.

## 기여

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다: `git checkout -b feature/새로운-기능`
3. 변경 사항을 커밋합니다: `git commit -m '새로운 기능 추가'`
4. 브랜치에 푸시합니다: `git push origin feature/새로운-기능`
5. Pull Request를 생성합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
