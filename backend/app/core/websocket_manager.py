from fastapi import WebSocket
from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store all active connections
        self.active_connections: List[WebSocket] = []
        # Map user_id to WebSockets (for user-specific notifications)
        self.user_connections: Dict[int, List[WebSocket]] = {}
        # Map ticker to WebSockets (for market data subscriptions)
        self.ticker_subscriptions: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
        logger.info("WebSocket connected")

    def disconnect(self, websocket: WebSocket, user_id: int = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
                
        # Remove from all subscriptions
        for ticker, clients in list(self.ticker_subscriptions.items()):
            if websocket in clients:
                clients.remove(websocket)
            if not clients:
                del self.ticker_subscriptions[ticker]
        
        logger.info("WebSocket disconnected")

    def subscribe(self, websocket: WebSocket, ticker: str):
        if ticker not in self.ticker_subscriptions:
            self.ticker_subscriptions[ticker] = set()
        self.ticker_subscriptions[ticker].add(websocket)
        logger.debug(f"Subscribed to {ticker}")

    def unsubscribe(self, websocket: WebSocket, ticker: str):
        if ticker in self.ticker_subscriptions and websocket in self.ticker_subscriptions[ticker]:
            self.ticker_subscriptions[ticker].remove(websocket)
            if not self.ticker_subscriptions[ticker]:
                del self.ticker_subscriptions[ticker]
            logger.debug(f"Unsubscribed from {ticker}")

    async def broadcast_to_ticker(self, ticker: str, data: dict):
        if ticker in self.ticker_subscriptions:
            dead_sockets = []
            for ws in self.ticker_subscriptions[ticker]:
                try:
                    await ws.send_json(data)
                except Exception:
                    dead_sockets.append(ws)
            for ws in dead_sockets:
                self.disconnect(ws)

manager = ConnectionManager()
