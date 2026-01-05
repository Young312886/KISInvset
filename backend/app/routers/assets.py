from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import account_schema, asset_schema
from ..services.asset_service import AccountService, AssetService

router = APIRouter()

# This would come from a dependency that gets the current user from a token
def get_current_user_id():
    return 1 # Hardcoded user ID for demonstration

@router.post("/accounts", response_model=account_schema.Account, status_code=201)
def create_user_account(
    account: account_schema.AccountCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Creates a new KIS account for the current user.
    (User is hardcoded to 1 for now).
    """
    service = AccountService(db)
    return service.create_account(user_id=user_id, account=account)

@router.get("/accounts", response_model=List[account_schema.Account])
def get_user_accounts(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Retrieves all KIS accounts for the current user.
    (User is hardcoded to 1 for now).
    """
    service = AccountService(db)
    return service.get_user_accounts(user_id=user_id)

@router.post("/accounts/{account_id}/assets", response_model=asset_schema.Asset, status_code=201)
def add_asset_to_account(
    account_id: int,
    asset: asset_schema.AssetCreate,
    db: Session = Depends(get_db)
):
    """
    Adds a new asset to a specific account.
    """
    service = AssetService(db)
    created_asset = service.add_asset_to_account(account_id=account_id, asset=asset)
    if not created_asset:
        raise HTTPException(status_code=404, detail="Account not found.")
    return created_asset

@router.get("/accounts/{account_id}/assets", response_model=List[asset_schema.Asset])
def get_account_assets(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves all assets for a specific account.
    """
    service = AssetService(db)
    return service.get_assets_for_account(account_id=account_id)
