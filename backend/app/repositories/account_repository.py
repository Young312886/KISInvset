from sqlalchemy.orm import Session
from typing import List

from ..database.models import KisAccount, Asset
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
