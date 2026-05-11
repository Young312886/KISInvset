from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.connection import get_db
from ..database.models import User
from ..api.dependencies import get_current_user
from ..schemas.watchlist_schema import WatchlistItem, WatchlistItemCreate
from ..repositories.watchlist_repository import WatchlistRepository

router = APIRouter()

@router.get("/", response_model=List[WatchlistItem])
def get_my_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """현재 로그인된 사용자의 관심 종목 목록을 조회합니다."""
    repo = WatchlistRepository(db)
    return repo.get_user_watchlist(current_user.id)

@router.post("/", response_model=WatchlistItem, status_code=status.HTTP_201_CREATED)
def add_stock_to_watchlist(
    item: WatchlistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """현재 로그인된 사용자의 관심 종목에 새로운 종목을 추가합니다."""
    repo = WatchlistRepository(db)
    # 이미 존재하는지 확인 (Optional but good practice)
    existing = db.query(User).filter(User.id == current_user.id).first().watchlist
    if any(i.symbol == item.symbol for i in existing):
        raise HTTPException(status_code=400, detail="Already in watchlist")
        
    return repo.add_to_watchlist(current_user.id, item.symbol, item.company_name)

@router.delete("/{symbol}")
def remove_stock_from_watchlist(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """현재 로그인된 사용자의 관심 종목에서 특정 종목을 제거합니다."""
    repo = WatchlistRepository(db)
    success = repo.remove_from_watchlist(current_user.id, symbol)
    if not success:
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")
    return {"message": f"Successfully removed {symbol} from watchlist"}
