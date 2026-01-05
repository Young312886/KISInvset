from sqlalchemy.orm import Session
from typing import List

from ..repositories.account_repository import AccountRepository, AssetRepository
from ..schemas import account_schema, asset_schema
from ..database.models import KisAccount, Asset

# IMPORTANT: This is a placeholder. In a real application, use a robust
# encryption library like 'cryptography'.
def _encrypt_key(key: str) -> str:
    return f"encrypted_{key}"

def _decrypt_key(key: str) -> str:
    return key.replace("encrypted_", "")


class AccountService:
    def __init__(self, db: Session):
        self.db = db
        self.account_repo = AccountRepository(db)

    def create_account(self, user_id: int, account: account_schema.AccountCreate) -> KisAccount:
        # In a real app, you'd get the user_id from an auth token
        encrypted_key = _encrypt_key(account.app_key)
        encrypted_secret = _encrypt_key(account.app_secret)
        return self.account_repo.create_account(
            user_id=user_id, 
            account=account,
            encrypted_key=encrypted_key,
            encrypted_secret=encrypted_secret
        )

    def get_user_accounts(self, user_id: int) -> List[KisAccount]:
        return self.account_repo.get_accounts_by_user(user_id=user_id)


class AssetService:
    def __init__(self, db: Session):
        self.db = db
        self.asset_repo = AssetRepository(db)
        self.account_repo = AccountRepository(db)

    def add_asset_to_account(self, account_id: int, asset: asset_schema.AssetCreate) -> Asset:
        # Check if account exists
        account = self.account_repo.get_account(account_id)
        if not account:
            return None # Or raise an exception
        return self.asset_repo.create_asset(account_id=account_id, asset=asset)

    def get_assets_for_account(self, account_id: int) -> List[Asset]:
        return self.asset_repo.get_assets_by_account(account_id=account_id)
