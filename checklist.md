# 프로젝트 설정 및 배포 체크리스트

이 문서는 '일목균형표 기반 실시간 투자 보조 웹 애플리케이션' 프로젝트의 남은 설정, 배포, 향후 개선 작업을 위한 체크리스트입니다.

### ✅ 1. 로컬 환경 설정

- [ ] **`.env` 파일 생성 및 설정**:
  - `backend` 폴더의 `.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.
  - 파일 내의 `KIS_APP_KEY`, `KIS_APP_SECRET`, `KIS_ACCOUNT_NO`를 실제 값으로 채웁니다.
  - 로컬 PostgreSQL 데이터베이스를 설정하고, `DATABASE_URL`을 실제 접속 정보로 수정합니다.

- [ ] **백엔드 의존성 설치**:
  ```bash
  # backend 폴더로 이동
  cd backend
  # 가상환경 생성 및 활성화 (권장)
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  # venv\Scripts\activate    # Windows
  # 의존성 설치
  pip install -r requirements.txt
  ```

- [ ] **프론트엔드 의존성 설치**:
  ```bash
  # frontend 폴더로 이동
  cd frontend
  # 의존성 설치
  npm install
  ```

- [ ] **데이터베이스 테이블 생성**:
  - 백엔드 서버를 처음 실행하면(`uvicorn backend.app.main:app --reload`), FastAPI 애플리케이션이 시작되면서 `models.py`에 정의된 모든 테이블이 자동으로 생성됩니다.

### ✅ 2. GitHub에 프로젝트 업로드

- [ ] **GitHub 저장소 생성**:
  - [GitHub.com](https://github.com)에서 `kis-invest-app`과 같은 이름으로 새로운 Public 저장소를 생성합니다.

- [ ] **Git 명령어 실행**:
  - 프로젝트 최상위 폴더(`C:\Code\KIS Invest`)에서 아래 명령어를 순서대로 실행하여 코드를 푸시합니다.
  ```bash
  git init
  git add .
  git commit -m "Initial commit: Full backend and frontend structure"
  git branch -M main
  git remote add origin https://github.com/YourUsername/YourRepositoryName.git
  git push -u origin main
  ```
  - `YourUsername`과 `YourRepositoryName`은 실제 정보로 변경해야 합니다.

### ✅ 3. 백엔드 배포 (Heroku)

- [ ] **Heroku 가입 및 CLI 설치**:
  - [Heroku](https://www.heroku.com/)에 가입합니다.
  - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)를 컴퓨터에 설치합니다.

- [ ] **Heroku 앱 생성 및 배포**:
  ```bash
  # Heroku 로그인
  heroku login
  # Heroku 앱 생성 (앱 이름은 자동으로 생성됨)
  heroku create
  # Heroku에 PostgreSQL 애드온 추가 (무료 플랜)
  heroku addons:create heroku-postgresql:hobby-dev
  ```

- [ ] **Heroku 환경 변수 설정**:
  - Heroku 대시보드 > `Settings` > `Config Vars`에서 아래 변수들을 설정합니다.
    - `KIS_APP_KEY`
    - `KIS_APP_SECRET`
    - `KIS_ACCOUNT_NO`
  - `DATABASE_URL`은 PostgreSQL 애드온 추가 시 자동으로 설정됩니다.

- [ ] **Heroku에 코드 푸시하여 배포**:
  ```bash
  # Heroku를 remote로 추가 (heroku create 시 자동으로 추가되었을 수 있음)
  # git remote add heroku <Heroku 앱의 Git URL>
  # Heroku에 main 브랜치를 푸시하여 배포
  git push heroku main
  ```

### ✅ 4. 프론트엔드 배포 (Vercel)

- [ ] **Vercel 가입**:
  - [Vercel](https://vercel.com/)에 GitHub 계정으로 가입합니다.

- [ ] **프로젝트 가져오기 및 배포**:
  - Vercel 대시보드에서 `Add New...` > `Project`를 선택합니다.
  - GitHub 저장소 목록에서 방금 생성한 `kis-invest-app`을 `Import` 합니다.
  - 프레임워크가 `Create React App`으로 자동 감지됩니다. `Root Directory`가 `frontend`로 설정되었는지 확인합니다.
  - `Environment Variables` 섹션을 열고, 아래 환경 변수를 추가합니다.
    - **Name**: `REACT_APP_API_URL`
    - **Value**: 위에서 배포한 Heroku 백엔드 앱의 URL (예: `https://your-heroku-app-name.herokuapp.com`)
  - `Deploy` 버튼을 클릭합니다.

### ✅ 5. 향후 개선 사항

- [ ] **사용자 인증 구현**:
  - 현재 하드코딩된 `user_id` 대신, JWT 토큰 기반의 회원가입 및 로그인 기능을 구현합니다.

- [ ] **4시간봉 데이터 처리**:
  - KIS API의 분봉 데이터를 가져와 4시간봉으로 리샘플링(resampling)하는 로직을 백엔드에 추가합니다.

- [ ] **분석 로직 고도화**:
  - 단순 골든/데드 크로스 외에 구름대 돌파, 쿠모 트위스트 등 더 복잡한 일목균형표 시그널 로직을 추가합니다.

- [ ] **API 키 암호화 강화**:
  - 현재의 임시 암호화 함수 대신, `cryptography` 라이브러리를 사용하여 안전하게 API 키를 암호화 및 복호화합니다.

- [ ] **테스트 코드 작성**:
  - 백엔드의 각 서비스와 엔드포인트에 대한 단위 테스트 및 통합 테스트를 작성하여 안정성을 높입니다.

- [ ] **UI/UX 개선**:
  - 프론트엔드 디자인을 다듬고 사용자 경험을 개선합니다.
