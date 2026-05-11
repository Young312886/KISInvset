from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..api.kis_api import KISApi
from ..schemas import market_schema

router = APIRouter()

# Initialize KIS API
kis_api = KISApi()

@router.get("/price/{symbol}", response_model=market_schema.StockPrice)
def get_stock_price(symbol: str):
    """
    Fetches real-time price for a specific stock symbol.
    """
    price_data = kis_api.get_current_price(symbol)
    if "error" in price_data and len(price_data) == 1:
        raise HTTPException(status_code=400, detail=price_data["error"])
    return price_data

@router.get("/prices", response_model=Dict[str, market_schema.StockPrice])
def get_multiple_prices(symbols: str):
    """
    Fetches real-time prices for multiple symbols (comma-separated) in parallel.
    """
    symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]
    if not symbol_list:
        return {}

    results = {}
    
    # Use ThreadPoolExecutor to fetch prices in parallel
    with ThreadPoolExecutor(max_workers=min(len(symbol_list), 10)) as executor:
        # Create a mapping of future to symbol
        future_to_symbol = {executor.submit(kis_api.get_current_price, symbol): symbol for symbol in symbol_list}
        
        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            try:
                results[symbol] = future.result()
            except Exception as e:
                results[symbol] = {"symbol": symbol, "error": str(e)}
                
    return results


@router.get("/indices")
def get_indices():
    """
    Fetches real-time prices for KOSPI and KOSDAQ.
    """
    kospi = kis_api.get_index_price("0001")
    kosdaq = kis_api.get_index_price("1001")
    return {
        "KOSPI": kospi,
        "KOSDAQ": kosdaq
    }
