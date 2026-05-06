"""
Pydantic schemas for User authentication endpoints.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Request Schemas (Client -> Server)
# ---------------------------------------------------------------------------

class UserRegisterRequest(BaseModel):
    """회원가입 요청 스키마"""
    username: str = Field(..., min_length=2, max_length=100, description="사용자 이름 (2~100자)")
    email: EmailStr = Field(..., description="이메일 주소 (로그인 ID로 사용)")
    password: str = Field(..., min_length=8, description="비밀번호 (8자 이상)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "홍길동",
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }
    }


class UserLoginRequest(BaseModel):
    """로그인 요청 스키마 (OAuth2 form 형식과 별도로 JSON도 지원)"""
    email: EmailStr = Field(..., description="이메일 주소")
    password: str = Field(..., description="비밀번호")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }
    }


# ---------------------------------------------------------------------------
# Response Schemas (Server -> Client)
# ---------------------------------------------------------------------------

class TokenResponse(BaseModel):
    """로그인 성공 시 반환되는 JWT 토큰 스키마"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """사용자 정보 응답 스키마 (비밀번호 제외)"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserRegisterResponse(BaseModel):
    """회원가입 성공 응답"""
    message: str = "회원가입이 완료되었습니다."
    user: UserResponse
