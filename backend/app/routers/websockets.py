from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/market")
async def websocket_market_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")
                ticker = message.get("ticker")
                
                if action == "subscribe" and ticker:
                    # If this is the first client subscribing to this ticker, tell KIS stream
                    is_new_ticker = ticker not in manager.ticker_subscriptions or not manager.ticker_subscriptions[ticker]
                    
                    manager.subscribe(websocket, ticker)
                    await websocket.send_json({"status": "subscribed", "ticker": ticker})
                    
                    if is_new_ticker:
                        from app.services.market_stream_service import market_stream
                        import asyncio
                        asyncio.create_task(market_stream.subscribe(ticker))
                        
                elif action == "unsubscribe" and ticker:
                    manager.unsubscribe(websocket, ticker)
                    await websocket.send_json({"status": "unsubscribed", "ticker": ticker})
                else:
                    await websocket.send_json({"status": "error", "message": "Unknown action or missing ticker"})
            except json.JSONDecodeError:
                await websocket.send_json({"status": "error", "message": "Invalid JSON format"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
