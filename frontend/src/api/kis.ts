const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export interface SignalData {
    id: number;
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
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
    tenkan_sen?: number;
    kijun_sen?: number;
    senkou_span_a?: number;
    senkou_span_b?: number;
    chikou_span?: number;
}


export const generateSignal = async (symbol: string): Promise<SignalData> => {
    const response = await fetch(`${API_BASE_URL}/signals/generate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: symbol, timeframe: 'D' }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate signal");
    }

    return response.json();
};

export const getChartData = async (symbol: string): Promise<ChartData[]> => {
    const response = await fetch(`${API_BASE_URL}/signals/${symbol}/chart?timeframe=D`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to fetch chart data");
    }

    return response.json();
};
