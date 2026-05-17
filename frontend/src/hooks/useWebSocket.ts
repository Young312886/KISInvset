import { useEffect, useRef, useCallback } from 'react';
import { useMarketStore } from '../store/marketStore';

const WS_URL = 'ws://localhost:8000/ws/market';

export const useWebSocket = () => {
  const ws = useRef<WebSocket | null>(null);
  const { setConnectionStatus, updatePrice, activeSubscriptions } = useMarketStore();
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) return;

    setConnectionStatus('connecting');
    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
      
      // Resubscribe to all active subscriptions upon reconnection
      activeSubscriptions.forEach(ticker => {
        socket.send(JSON.stringify({ action: 'subscribe', ticker }));
      });
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'realtime_price') {
          updatePrice({
            ticker: data.ticker,
            price: data.price,
            change: data.change,
            change_rate: data.change_rate,
            volume: data.volume
          });
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message', error);
      }
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
      ws.current = null;
      
      // Auto-reconnect after 3 seconds
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = setTimeout(() => {
        connect();
      }, 3000);
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error', error);
    };

    ws.current = socket;
  }, [setConnectionStatus, updatePrice, activeSubscriptions]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [connect]);

  const subscribe = useCallback((ticker: string) => {
    useMarketStore.getState().subscribeTicker(ticker);
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ action: 'subscribe', ticker }));
    }
  }, []);

  const unsubscribe = useCallback((ticker: string) => {
    useMarketStore.getState().unsubscribeTicker(ticker);
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ action: 'unsubscribe', ticker }));
    }
  }, []);

  return { subscribe, unsubscribe };
};
