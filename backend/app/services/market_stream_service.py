import asyncio
import json
import websockets
import logging
from app.core.config import settings
from app.api.kis_api import KISApi
from app.core.websocket_manager import manager

logger = logging.getLogger(__name__)

class MarketStreamService:
    def __init__(self):
        self.kis_api = KISApi()
        self.ws_url = "ws://ops.koreainvestment.com:31000" if "vts" in settings.KIS_BASE_URL else "ws://ops.koreainvestment.com:21000"
        self.connection = None
        self.running = False

    async def start(self):
        if self.running:
            return
            
        self.running = True
        asyncio.create_task(self._connect_and_listen())

    async def stop(self):
        self.running = False
        if self.connection:
            await self.connection.close()

    async def subscribe(self, ticker: str):
        if not self.connection:
            logger.warning("Stream not connected yet.")
            return

        # Fetching approval key using thread executor to not block the async loop
        loop = asyncio.get_event_loop()
        approval_key = await loop.run_in_executor(None, self.kis_api.get_ws_approval_key)
        
        if not approval_key:
            logger.error("Failed to get approval key for WebSocket")
            return
            
        subscription_data = {
            "header": {"approval_key": approval_key, "custtype": "P", "tr_type": "1", "content-type": "utf-8"},
            "body": {"input": {"tr_id": "H0STCNT0", "tr_key": ticker}}
        }
        await self.connection.send(json.dumps(subscription_data))
        logger.info(f"Subscribed to KIS stream for {ticker}")

    async def _connect_and_listen(self):
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    self.connection = ws
                    logger.info("Connected to KIS Real-time WebSocket")
                    
                    # Re-subscribe to all active tickers from manager
                    active_tickers = list(manager.ticker_subscriptions.keys())
                    for ticker in active_tickers:
                        await self.subscribe(ticker)
                        
                    while self.running:
                        message = await ws.recv()
                        await self._handle_message(message)
                        
            except websockets.exceptions.ConnectionClosed:
                logger.warning("KIS WebSocket connection closed. Reconnecting in 5 seconds...")
            except Exception as e:
                logger.error(f"KIS WebSocket Error: {e}")
            
            self.connection = None
            if self.running:
                await asyncio.sleep(5)

    async def _handle_message(self, message: str):
        if isinstance(message, bytes):
            message = message.decode('utf-8')
            
        if message[0] in ['0', '1']:
            parts = message.split('|')
            if len(parts) > 1 and parts[1] == "H0STCNT0":
                data = parts[3].split('^')
                if len(data) >= 7:
                    ticker = data[0]
                    # Parse real-time data
                    payload = {
                        "type": "realtime_price",
                        "ticker": ticker,
                        "price": float(data[2]),
                        "change": float(data[4]),
                        "change_rate": float(data[5]),
                        "volume": int(data[6])
                    }
                    await manager.broadcast_to_ticker(ticker, payload)
        elif message.startswith('{"'): 
            # System JSON messages like PINGPONG
            try:
                data = json.loads(message)
                if data.get("header", {}).get("tr_id") == "PINGPONG":
                    await self.connection.send(message) # PONG echo
            except json.JSONDecodeError:
                pass

market_stream = MarketStreamService()
