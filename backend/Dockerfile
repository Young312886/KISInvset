# 1. 공식 Python 런타임을 부모 이미지로 사용합니다.
FROM python:3.9-slim

# 2. 환경 변수를 설정합니다.
# Python이 .pyc 파일을 디스크에 쓰는 것을 방지합니다.
ENV PYTHONDONTWRITEBYTECODE 1
# Python 출력이 버퍼링 없이 바로 터미널로 전송되도록 합니다.
ENV PYTHONUNBUFFERED 1
# Cloud Run이 PORT 환경 변수를 제공합니다. 로컬 테스트를 위해 8080으로 기본 설정합니다.
ENV PORT 8080

# 3. 작업 디렉터리를 설정합니다.
WORKDIR /app

# 4. 의존성을 설치합니다.
# Docker 캐시를 활용하기 위해 requirements.txt 파일을 먼저 복사합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. 애플리케이션 코드를 복사합니다.
COPY ./app ./app

# 6. 앱이 실행될 포트를 노출합니다.
EXPOSE 8080

# 7. 애플리케이션을 실행합니다.
# PORT 환경 변수는 Cloud Run에 의해 자동으로 설정됩니다.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --worker-class uvicorn.workers.UvicornWorker app.main:app
