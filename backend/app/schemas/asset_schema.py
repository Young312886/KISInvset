from pydantic import BaseModel

class AssetBase(BaseModel):
    symbol: str
    quantity: int
    avg_purchase_price: float

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    account_id: int
    
    class Config:
        from_attributes = True
