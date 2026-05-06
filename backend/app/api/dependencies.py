"""
FastAPI Dependency functions for authentication.
Usage:
    @router.get("/me")
    def get_me(current_user: User = Depends(get_current_user)):
        ...
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import User
from ..core.security import decode_access_token

# OAuth2PasswordBearer: Authorization 헤더에서 Bearer 토큰을 자동으로 추출합니다.
# tokenUrl은 Swagger UI에서 "Authorize" 버튼이 토큰을 가져올 엔드포인트입니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Authorization 헤더의 Bearer 토큰을 검증하고 현재 사용자를 반환합니다.

    - 토큰이 없거나 유효하지 않으면 401 Unauthorized를 반환합니다.
    - 토큰에 해당하는 사용자가 DB에 없으면 401을 반환합니다.
    - 사용자 계정이 비활성화 상태면 403 Forbidden을 반환합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않거나 만료된 인증 토큰입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # JWT payload의 "sub" 필드에 이메일을 저장합니다.
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 사용자 계정입니다.",
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """get_current_user의 alias. 가독성을 위해 사용합니다."""
    return current_user
