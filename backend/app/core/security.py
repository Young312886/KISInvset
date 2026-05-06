"""
Security utilities: password hashing, JWT token creation, and Fernet API key encryption.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt
from cryptography.fernet import Fernet, InvalidToken

from .config import settings

# ---------------------------------------------------------------------------
# Password Hashing (bcrypt direct — passlib/Python 3.13 호환성 문제 우회)
# ---------------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    """Plain-text password를 Bcrypt 해시로 변환합니다."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호가 저장된 해시와 일치하는지 확인합니다."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ---------------------------------------------------------------------------
# JWT Token
# ---------------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT Access Token을 생성합니다.
    - data: 토큰에 담을 payload (예: {"sub": "user@email.com"})
    - expires_delta: 유효 기간 (기본값: settings의 설정값 사용)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    JWT Token을 디코딩합니다.
    유효하지 않거나 만료된 경우 None을 반환합니다.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Fernet Encryption (for KIS / DART API Keys)
# ---------------------------------------------------------------------------

def _get_fernet() -> Optional[Fernet]:
    """
    .env의 ENCRYPTION_KEY로 Fernet 인스턴스를 생성합니다.
    키가 없거나 유효하지 않으면 None을 반환합니다.
    """
    key = settings.ENCRYPTION_KEY
    if not key:
        return None
    try:
        return Fernet(key.encode())
    except Exception:
        return None


def encrypt_api_key(plain_text: str) -> str:
    """
    API Key를 Fernet으로 암호화하여 문자열로 반환합니다.
    ENCRYPTION_KEY가 없으면 평문을 그대로 반환합니다 (개발 편의용).
    """
    fernet = _get_fernet()
    if not fernet:
        return plain_text
    return fernet.encrypt(plain_text.encode()).decode()


def decrypt_api_key(encrypted_text: str) -> str:
    """
    Fernet으로 암호화된 API Key를 복호화하여 반환합니다.
    복호화 실패 시 빈 문자열을 반환합니다.
    """
    fernet = _get_fernet()
    if not fernet:
        return encrypted_text
    try:
        return fernet.decrypt(encrypted_text.encode()).decode()
    except InvalidToken:
        return ""
