from sqlalchemy.orm import Session
from typing import List

from ..database.models import KisAccount, Asset, TradeHistory
from ..schemas import account_schema, asset_schema

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, user_id: int, account: account_schema.AccountCreate, encrypted_key: str, encrypted_secret: str) -> KisAccount:
        db_account = KisAccount(
            user_id=user_id,
            account_number=account.account_number,
            app_key_encrypted=encrypted_key,
            app_secret_encrypted=encrypted_secret,
            is_active=account.is_active
        )
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account

    def get_account(self, account_id: int) -> KisAccount:
        return self.db.query(KisAccount).filter(KisAccount.id == account_id).first()

    def get_accounts_by_user(self, user_id: int) -> List[KisAccount]:
        return self.db.query(KisAccount).filter(KisAccount.user_id == user_id).all()

    def update_balance(self, account_id: int, amount_change: float) -> KisAccount:
        account = self.get_account(account_id)
        if account:
            account.balance = float(account.balance) + amount_change
            self.db.commit()
            self.db.refresh(account)
        return account

class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_asset(self, account_id: int, asset: asset_schema.AssetCreate) -> Asset:
        db_asset = Asset(**asset.model_dump(), account_id=account_id)
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_assets_by_account(self, account_id: int) -> List[Asset]:
        return self.db.query(Asset).filter(Asset.account_id == account_id).all()

    def get_asset_by_symbol(self, account_id: int, symbol: str) -> Asset:
        return self.db.query(Asset).filter(Asset.account_id == account_id, Asset.symbol == symbol).first()

    def update_asset(self, asset: Asset):
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete_asset(self, asset: Asset):
        self.db.delete(asset)
        self.db.commit()

    def create_trade_history(self, account_id: int, trade_data: dict) -> TradeHistory:
        db_trade = TradeHistory(
            account_id=account_id,
            symbol=trade_data['symbol'],
            company_name=trade_data.get('company_name', trade_data['symbol']),
            trade_type=trade_data['side'],
            quantity=trade_data['quantity'],
            price=trade_data['price'],
            commission=trade_data.get('commission', 0),
            tax=trade_data.get('tax', 0),
            memo=trade_data.get('memo', '')
        )
        self.db.add(db_trade)
        self.db.commit()
        self.db.refresh(db_trade)
        return db_trade
