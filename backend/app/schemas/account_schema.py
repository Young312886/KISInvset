from pydantic import BaseModel
from typing import List, Optional
from .asset_schema import Asset

class AccountBase(BaseModel):
    account_number: str
    is_active: bool = True

class AccountCreate(AccountBase):
    app_key: str
    app_secret: str

class Account(AccountBase):
    id: int
    user_id: int
    assets: List[Asset] = []

    class Config:
        from_attributes = True