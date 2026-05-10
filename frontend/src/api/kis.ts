const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

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
