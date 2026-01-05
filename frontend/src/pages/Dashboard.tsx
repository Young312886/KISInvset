import React, { useState } from 'react';
import { generateSignal, getChartData, SignalData, ChartData } from '../api/kis';
import IchimokuChart from '../components/IchimokuChart';

const Dashboard: React.FC = () => {
    const [symbol, setSymbol] = useState<string>('005930');
    const [signal, setSignal] = useState<SignalData | null>(null);
    const [chartData, setChartData] = useState<ChartData[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalysis = async () => {
        setLoading(true);
        setError(null);
        setSignal(null);
        setChartData([]);
        try {
            // Fetch both signal and chart data in parallel
            const [signalResult, chartResult] = await Promise.all([
                generateSignal(symbol),
                getChartData(symbol)
            ]);
            setSignal(signalResult);
            setChartData(chartResult);
        } catch (err: any) {
            setError(err.message || 'An unknown error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Ichimoku Signal Dashboard</h1>
            
            <div className="flex items-center space-x-2 mb-4">
                <input
                    type="text"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    className="border p-2 rounded w-40"
                    placeholder="e.g., 005930"
                />
                <button
                    onClick={handleAnalysis}
                    disabled={loading}
                    className="bg-blue-500 text-white p-2 rounded disabled:bg-gray-400"
                >
                    {loading ? 'Analyzing...' : 'Analyze'}
                </button>
            </div>

            {error && <div className="text-red-500 bg-red-100 p-3 rounded mb-4">{error}</div>}

            {signal && (
                <div className="bg-gray-100 p-4 rounded">
                    <h2 className="text-xl font-semibold">Analysis for {signal.symbol}</h2>
                    <div className="grid grid-cols-2 gap-4 mt-2">
                        <div>
                            <p><strong>Signal:</strong> 
                                <span className={`font-bold ${signal.signal === 'BUY' ? 'text-green-600' : signal.signal === 'SELL' ? 'text-red-600' : 'text-gray-700'}`}>
                                    {signal.signal}
                                </span>
                            </p>
                            <p><strong>Generated At:</strong> {new Date(signal.generated_at).toLocaleString()}</p>
                        </div>
                        <div className="text-sm">
                            <p><strong>Close:</strong> {signal.details.close}</p>
                            <p><strong>Tenkan-sen:</strong> {signal.details.tenkan_sen}</p>
                            <p><strong>Kijun-sen:</strong> {signal.details.kijun_sen}</p>
                        </div>
                    </div>
                </div>
            )}

            <div className="mt-4 border rounded p-4 bg-white">
                <h3 className="text-lg font-medium mb-2">Chart</h3>
                {loading && <div className="text-center p-8">Loading chart data...</div>}
                {chartData.length > 0 ? (
                    <IchimokuChart data={chartData} />
                ) : (
                    !loading && <div className="text-center p-8 text-gray-500">Click 'Analyze' to see the chart.</div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
