"""
Authentication router: /auth/register, /auth/login, /auth/me
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import User
from ..core.security import hash_password, verify_password, create_access_token
from ..api.dependencies import get_current_user
from ..schemas.user_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    UserRegisterResponse,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /auth/register — 회원가입
# ---------------------------------------------------------------------------
@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="이메일, 사용자 이름, 비밀번호로 새 계정을 생성합니다.",
)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 이메일입니다.",
        )
    # 사용자 이름 중복 확인
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 사용자 이름입니다.",
        )

    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserRegisterResponse(user=UserResponse.model_validate(new_user))


# ---------------------------------------------------------------------------
# POST /auth/login — 로그인 (JSON body)
# ---------------------------------------------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="로그인 (JSON)",
    description="이메일/비밀번호로 로그인하여 JWT Access Token을 발급받습니다.",
)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 사용자 계정입니다.",
        )

    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)


# ---------------------------------------------------------------------------
# POST /auth/token — Swagger UI용 OAuth2 로그인 (form-data)
# ---------------------------------------------------------------------------
@router.post(
    "/token",
    response_model=TokenResponse,
    include_in_schema=False,  # Swagger 목록에서 숨김 (내부 전용)
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Swagger UI의 'Authorize' 버튼이 사용하는 OAuth2 form-data 로그인 엔드포인트."""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)


# ---------------------------------------------------------------------------
# GET /auth/me — 현재 로그인된 사용자 정보 조회
# ---------------------------------------------------------------------------
@router.get(
    "/me",
    response_model=UserResponse,
    summary="내 정보 조회",
    description="현재 로그인된 사용자의 정보를 반환합니다. JWT 토큰이 필요합니다.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
