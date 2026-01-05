import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from the parent directory of the app
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))

class Settings(BaseSettings):
    # KIS API Credentials
    KIS_APP_KEY: str
    KIS_APP_SECRET: str
    KIS_ACCOUNT_NO: str

    # KIS API URL
    KIS_BASE_URL: str = "https://openapivts.koreainvestment.com:29443" # Default to mock trading

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # This is to tell pydantic to look for the .env file in the backend directory
        # when the script is run from the root.
        # However, the load_dotenv call above is more explicit and reliable.
        case_sensitive = True

settings = Settings()
