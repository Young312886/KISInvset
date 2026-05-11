from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import trade_history_schema
from ..repositories.trade_history_repository import TradeHistoryRepository
from ..api.dependencies import get_current_user
from ..database.models import User

router = APIRouter()

@router.get("/", response_model=List[trade_history_schema.TradeHistory])
def get_my_trade_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the recent trade history for the current user.
    """
    repo = TradeHistoryRepository(db)
    return repo.get_all_by_user(user_id=current_user.id, limit=limit)

@router.get("/account/{account_id}", response_model=List[trade_history_schema.TradeHistory])
def get_account_trade_history(
    account_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the recent trade history for a specific account.
    """
    repo = TradeHistoryRepository(db)
    # TODO: Verify account belongs to user
    return repo.get_by_account(account_id=account_id, limit=limit)
