import { create } from 'zustand';

export interface RealtimePriceData {
  ticker: string;
  price: number;
  change: number;
  change_rate: number;
  volume: number;
  timestamp: number;
}

interface MarketStore {
  realtimePrices: Record<string, RealtimePriceData>;
  connectionStatus: 'connecting' | 'connected' | 'disconnected';
  setConnectionStatus: (status: 'connecting' | 'connected' | 'disconnected') => void;
  updatePrice: (data: Omit<RealtimePriceData, 'timestamp'>) => void;
  subscribeTicker: (ticker: string) => void;
  unsubscribeTicker: (ticker: string) => void;
  activeSubscriptions: Set<string>;
}

export const useMarketStore = create<MarketStore>((set) => ({
  realtimePrices: {},
  connectionStatus: 'disconnected',
  activeSubscriptions: new Set(),
  
  setConnectionStatus: (status) => set({ connectionStatus: status }),
  
  updatePrice: (data) => set((state) => ({
    realtimePrices: {
      ...state.realtimePrices,
      [data.ticker]: { ...data, timestamp: Date.now() }
    }
  })),

  subscribeTicker: (ticker) => set((state) => {
    const newSubs = new Set(state.activeSubscriptions);
    newSubs.add(ticker);
    return { activeSubscriptions: newSubs };
  }),

  unsubscribeTicker: (ticker) => set((state) => {
    const newSubs = new Set(state.activeSubscriptions);
    newSubs.delete(ticker);
    return { activeSubscriptions: newSubs };
  }),
}));
