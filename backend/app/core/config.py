import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from the backend directory (parent of app/)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))

class Settings(BaseSettings):
    # KIS API Credentials
    KIS_APP_KEY: str = "dummy_key"
    KIS_APP_SECRET: str = "dummy_secret"
    KIS_ACCOUNT_NO: str = "dummy_account"

    # KIS API URL
    KIS_BASE_URL: str = "https://openapivts.koreainvestment.com:29443"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/kis_invest"

    # Open DART API Key (재무 데이터)
    DART_API_KEY: str = ""

    # JWT Authentication
    JWT_SECRET_KEY: str = "change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # API Key Encryption (Fernet)
    ENCRYPTION_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
