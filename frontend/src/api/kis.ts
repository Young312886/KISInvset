const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
};


export interface SignalData {
    id?: number;
    symbol: string;
    timeframe: string;
    signal: string;
    details: {
        tenkan_sen: number;
        kijun_sen: number;
        senkou_span_a: number;
        senkou_span_b: number;
        close: number;
    };
    generated_at: string;
}

export interface ChartData {
    time: number;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
    tenkan_sen?: number;
    kijun_sen?: number;
    senkou_span_a?: number;
    senkou_span_b?: number;
}

export interface FundamentalScore {
    ticker: string;
    total_score: number;
    profitability_score: number;
    value_score: number;
    growth_score: number;
    safety_score: number;
    dividend_score: number;
    grade: string;
    updated_at: string;
}

export interface WatchlistItem {
    id: number;
    symbol: string;
    company_name: string;
    added_at: string;
}


export const generateSignal = async (symbol: string): Promise<SignalData> => {
    const response = await fetch(`${API_BASE_URL}/signals/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol, timeframe: 'D' }),
    });
    if (!response.ok) throw new Error("Failed to generate signal");
    return response.json();
};

export const getChartData = async (symbol: string, timeframe: string = 'D'): Promise<ChartData[]> => {
    // Return dummy data if API fails to allow UI to render (for dev purposes)
    try {
        const response = await fetch(`${API_BASE_URL}/signals/${symbol}/chart?timeframe=${timeframe}`);
        if (!response.ok) throw new Error("Failed to fetch chart data");
        const data = await response.json();
        // Convert date string to unix timestamp for lightweight-charts
        return data.map((d: any) => ({
            ...d,
            time: new Date(d.date).getTime() / 1000
        }));
    } catch (e) {
        console.warn("Using mock chart data due to API error", e);
        return Array.from({ length: 100 }).map((_, i) => {
            const close = 80000 + Math.random() * 5000;
            return {
                time: (new Date().getTime() / 1000) - (100 - i) * 86400,
                open: close - 500,
                high: close + 1000,
                low: close - 1000,
                close,
                volume: 1000000,
                tenkan_sen: close - 100,
                kijun_sen: close - 200,
                senkou_span_a: close - 300,
                senkou_span_b: close - 400
            };
        });
    }
};

export const getFundamentalScore = async (symbol: string): Promise<FundamentalScore> => {
    try {
        const response = await fetch(`${API_BASE_URL}/fundamentals/${symbol}/score`);
        if (!response.ok) throw new Error("Failed to fetch fundamental score");
        return response.json();
    } catch (e) {
        console.warn("Using mock fundamental data due to API error", e);
        return {
            ticker: symbol,
            total_score: 78,
            profitability_score: 85,
            value_score: 70,
            growth_score: 65,
            safety_score: 90,
            dividend_score: 60,
            grade: 'BUY',
            updated_at: new Date().toISOString()
        };
    }
};

export const getWatchlist = async (): Promise<WatchlistItem[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/watchlist/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Failed to fetch watchlist");
        return response.json();
    } catch (e) {
        console.warn("Using mock watchlist data due to API error", e);
        return [
            { id: 1, symbol: '005930', company_name: '삼성전자', added_at: new Date().toISOString() },
            { id: 2, symbol: '000660', company_name: 'SK하이닉스', added_at: new Date().toISOString() },
            { id: 3, symbol: '035420', company_name: 'NAVER', added_at: new Date().toISOString() },
        ];
    }
};

export const addToWatchlist = async (symbol: string, company_name?: string): Promise<WatchlistItem> => {
    const response = await fetch(`${API_BASE_URL}/watchlist/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ symbol, company_name }),
    });
    if (!response.ok) throw new Error("Failed to add to watchlist");
    return response.json();
};

export const removeFromWatchlist = async (symbol: string): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/watchlist/${symbol}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error("Failed to remove from watchlist");
};

export interface PortfolioAsset {
    id: number;
    symbol: string;
    company_name: string;
    quantity: number;
    avg_purchase_price: number;
    current_price?: number;
    pnl_amount: number;
    pnl_rate: number;
}

export const getPortfolioAssets = async (accountId: number): Promise<PortfolioAsset[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/assets/accounts/${accountId}/assets`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Failed to fetch portfolio assets");
        return response.json();
    } catch (e) {
        console.warn("Using mock portfolio data due to API error", e);
        return [
            { id: 1, symbol: '005930', company_name: '삼성전자', quantity: 10, avg_purchase_price: 75000, current_price: 82300 },
            { id: 2, symbol: '000660', company_name: 'SK하이닉스', quantity: 5, avg_purchase_price: 160000, current_price: 178500 },
            { id: 3, symbol: '035420', company_name: 'NAVER', quantity: 20, avg_purchase_price: 200000, current_price: 192000 },
        ];
    }
};

export interface TradeEntry {
    id: number;
    symbol: string;
    company_name: string;
    trade_type: 'BUY' | 'SELL';
    quantity: number;
    price: number;
    traded_at: string;
}

export const getTradeHistory = async (limit: number = 20): Promise<TradeEntry[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/trade-history/?limit=${limit}`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Failed to fetch trade history");
        return response.json();
    } catch (e) {
        console.warn("Using mock trade history due to API error", e);
        return [
            { id: 1, symbol: '005930', company_name: '삼성전자', trade_type: 'BUY', quantity: 10, price: 75000, traded_at: new Date().toISOString() },
            { id: 2, symbol: '000660', company_name: 'SK하이닉스', trade_type: 'SELL', quantity: 5, price: 180000, traded_at: new Date(Date.now() - 86400000).toISOString() },
        ];
    }
};

export interface StockPrice {
    symbol: string;
    current_price: number;
    change: number;
    change_rate: number;
    volume: number;
    high: number;
    low: number;
    open: number;
    last_updated?: string;
    error?: string;
}

export const getStockPrice = async (symbol: string): Promise<StockPrice> => {
    const response = await fetch(`${API_BASE_URL}/market/price/${symbol}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch stock price");
    return response.json();
};

export const getMultiplePrices = async (symbols: string[]): Promise<Record<string, StockPrice>> => {
    if (symbols.length === 0) return {};
    const response = await fetch(`${API_BASE_URL}/market/prices?symbols=${symbols.join(',')}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch multiple stock prices");
    return response.json();
};

export const getMarketIndices = async (): Promise<any> => {
    try {
        const response = await fetch(`${API_BASE_URL}/market/indices`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error("Failed to fetch market indices");
        return response.json();
    } catch (e) {
        console.warn("Using mock indices due to API error", e);
        return {
            KOSPI: { current_price: 2750.42, change: 12.5, change_rate: 0.45 },
            KOSDAQ: { current_price: 890.15, change: -2.3, change_rate: -0.26 }
        };
    }
};

export interface BacktestResult {
    symbol: string;
    initial_cash: number;
    final_value: number;
    total_return_pct: number;
    mdd_pct: number;
    trades_count: number;
    history: { date: string, value: number, price: number }[];
    trades: any[];
}

export const runBacktest = async (
    symbol: string, 
    startDate: string, 
    endDate: string, 
    strategy: string = 'sma_crossover'
): Promise<BacktestResult> => {
    const response = await fetch(
        `${API_BASE_URL}/backtest/run?symbol=${symbol}&start_date=${startDate}&end_date=${endDate}&strategy=${strategy}`,
        { headers: getAuthHeaders() }
    );
    if (!response.ok) throw new Error("Backtest failed");
    return response.json();
};

