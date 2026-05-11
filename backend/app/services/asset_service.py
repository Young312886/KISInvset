from sqlalchemy.orm import Session
from typing import List

from ..repositories.account_repository import AccountRepository, AssetRepository
from ..schemas import account_schema, asset_schema
from ..database.models import KisAccount, Asset

from cryptography.fernet import Fernet
from ..core.config import settings

def _get_cipher():
    # If encryption key is not set, we should probably log a warning
    # and use a fallback for dev, but in production this is critical.
    key = settings.ENCRYPTION_KEY
    if not key:
        # Generate a temporary key for dev if not provided
        # NOTE: This will make previously stored keys unreadable if restarted!
        return Fernet(Fernet.generate_key())
    return Fernet(key.encode())

def _encrypt_key(key: str) -> str:
    if not key: return ""
    cipher = _get_cipher()
    return cipher.encrypt(key.encode()).decode()

def _decrypt_key(encrypted_key: str) -> str:
    if not encrypted_key: return ""
    cipher = _get_cipher()
    try:
        return cipher.decrypt(encrypted_key.encode()).decode()
    except Exception:
        return encrypted_key # Fallback for non-encrypted keys during migration



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


from ..api.kis_api import KISApi
from ..core.config import settings

class AssetService:
    def __init__(self, db: Session):
        self.db = db
        self.asset_repo = AssetRepository(db)
        self.account_repo = AccountRepository(db)
        self.kis_api = KISApi()

    def add_asset_to_account(self, account_id: int, asset: asset_schema.AssetCreate) -> Asset:
        # Check if account exists
        account = self.account_repo.get_account(account_id)
        if not account:
            return None # Or raise an exception
        return self.asset_repo.create_asset(account_id=account_id, asset=asset)

    def get_assets_for_account(self, account_id: int) -> List[dict]:
        assets = self.asset_repo.get_assets_by_account(account_id=account_id)
        
        result = []
        for asset in assets:
            asset_dict = {
                "id": asset.id,
                "account_id": asset.account_id,
                "symbol": asset.symbol,
                "company_name": asset.company_name,
                "quantity": asset.quantity,
                "avg_purchase_price": float(asset.avg_purchase_price),
                "current_price": 0.0,
                "pnl_amount": 0.0,
                "pnl_rate": 0.0
            }
            try:
                price_data = self.kis_api.get_current_price(asset.symbol)
                curr_price = float(price_data['current_price'])
                asset_dict["current_price"] = curr_price
                
                # P&L Calculation
                total_cost = asset.quantity * float(asset.avg_purchase_price)
                total_value = asset.quantity * curr_price
                asset_dict["pnl_amount"] = total_value - total_cost
                if total_cost > 0:
                    asset_dict["pnl_rate"] = ((total_value / total_cost) - 1) * 100
                    
            except Exception as e:
                print(f"Error fetching price for {asset.symbol}: {e}")
            
            result.append(asset_dict)
        
        return result

    def execute_trade(self, account_id: int, trade_data: dict) -> Asset:
        """
        Executes a trade: updates quantity and average purchase price (WAC).
        trade_data: { symbol, company_name, quantity, price, side: 'BUY'|'SELL', order_type: '00'|'01' }
        """
        symbol = trade_data['symbol']
        quantity = trade_data['quantity']
        price = trade_data['price']
        side = trade_data['side']
        
        # 1. Fetch account and check type
        account = self.account_repo.get_account(account_id)
        if not account:
            raise ValueError("Account not found.")

        # 2. Real-world execution if applicable
        if account.account_type == 'REAL':
            # Extract CANO and ACNT_PRDT_CD (format usually: 12345678-01)
            acc_parts = account.account_number.split('-')
            cano = acc_parts[0]
            prdt_cd = acc_parts[1] if len(acc_parts) > 1 else "01"
            
            order_type = trade_data.get('order_type', '01') # Default to Limit
            
            res = self.kis_api.place_order(
                account_no=cano,
                account_product_code=prdt_cd,
                symbol=symbol,
                order_type=order_type,
                price=int(price),
                quantity=quantity,
                order_side=side
            )
            
            if res.get('rt_cd') != '0':
                raise ValueError(f"KIS API Order Failed: {res.get('msg1')}")
            
            # For REAL accounts, we might want to update ledger based on API response
            # but for now, we continue with local balance tracking as well.

        existing_asset = self.asset_repo.get_asset_by_symbol(account_id, symbol)
        total_amount = quantity * price
        
        updated_asset = None
        if side == 'BUY':
            # Check balance
            if float(account.balance) < total_amount:
                raise ValueError("Insufficient balance for this trade.")
            
            # Deduct balance
            self.account_repo.update_balance(account_id, -total_amount)

            if existing_asset:
                # WAC Calculation: (Q1*P1 + Q2*P2) / (Q1 + Q2)
                old_qty = existing_asset.quantity
                old_avg = float(existing_asset.avg_purchase_price)
                
                new_qty = old_qty + quantity
                new_avg = ((old_qty * old_avg) + (quantity * price)) / new_qty
                
                existing_asset.quantity = new_qty
                existing_asset.avg_purchase_price = new_avg
                updated_asset = self.asset_repo.update_asset(existing_asset)
            else:
                # Create new asset
                new_asset_data = asset_schema.AssetCreate(
                    symbol=symbol,
                    company_name=trade_data.get('company_name', symbol),
                    quantity=quantity,
                    avg_purchase_price=price
                )
                updated_asset = self.asset_repo.create_asset(account_id, new_asset_data)
        
        elif side == 'SELL':
            if not existing_asset or existing_asset.quantity < quantity:
                raise ValueError("Insufficient quantity to sell.")
            
            # Add balance
            self.account_repo.update_balance(account_id, total_amount)

            existing_asset.quantity -= quantity
            if existing_asset.quantity == 0:
                self.asset_repo.delete_asset(existing_asset)
                updated_asset = None
            else:
                updated_asset = self.asset_repo.update_asset(existing_asset)
        
        # 3. Log trade history
        self.asset_repo.create_trade_history(account_id, trade_data)
        
        return updated_asset
