import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import { 
  Play, 
  TrendingUp, 
  TrendingDown, 
  BarChart3, 
  Calendar,
  AlertCircle,
  CheckCircle2,
  Clock
} from 'lucide-react';
import { runBacktest } from '../api/kis';

const BacktestReport: React.FC = () => {
  const [symbol, setSymbol] = useState('005930');
  const [strategy, setStrategy] = useState('SMA_CROSSOVER');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunBacktest = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const endDateObj = new Date();
      const startDateObj = new Date();
      startDateObj.setFullYear(endDateObj.getFullYear() - 1);
      const startDate = startDateObj.toISOString().split('T')[0];
      const endDate = endDateObj.toISOString().split('T')[0];
      
      const data = await runBacktest(symbol, startDate, endDate, strategy);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Backtest failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Strategy Backtesting Engine
          </h1>
          <p className="text-slate-500 text-sm">Analyze strategy performance on historical data</p>
        </div>
        
        <div className="flex flex-wrap gap-3">
          <div className="flex flex-col">
            <label className="text-xs font-semibold text-slate-400 mb-1">Symbol</label>
            <input 
              type="text" 
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="e.g. 005930"
              className="px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>
          
          <div className="flex flex-col">
            <label className="text-xs font-semibold text-slate-400 mb-1">Strategy</label>
            <select 
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option value="SMA_CROSSOVER">SMA Crossover</option>
              <option value="RSI_STRATEGY">RSI Overbought/Oversold</option>
            </select>
          </div>

          <button 
            onClick={handleRunBacktest}
            disabled={isLoading}
            className={`mt-auto flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-all shadow-lg shadow-blue-500/20 disabled:opacity-50 ${isLoading ? 'animate-pulse' : ''}`}
          >
            {isLoading ? <Clock size={16} /> : <Play size={16} />}
            {isLoading ? 'Running...' : 'Run Analysis'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 rounded-xl flex items-center gap-3 text-red-600">
          <AlertCircle size={20} />
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      {result && (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-800 p-5 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <p className="text-slate-500 text-sm font-medium">Total Return</p>
                <div className={`p-2 rounded-lg ${result.total_return_pct >= 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'}`}>
                  <TrendingUp size={16} />
                </div>
              </div>
              <h3 className={`text-2xl font-bold ${result.total_return_pct >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                {result.total_return_pct.toFixed(2)}%
              </h3>
              <p className="text-xs text-slate-400 mt-1">Benchmark: {result.benchmark_return_pct.toFixed(2)}%</p>
            </div>

            <div className="bg-white dark:bg-slate-800 p-5 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <p className="text-slate-500 text-sm font-medium">Win Rate</p>
                <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                  <CheckCircle2 size={16} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                {result.win_rate.toFixed(1)}%
              </h3>
              <p className="text-xs text-slate-400 mt-1">{result.trades.filter((t:any)=>t.profit > 0).length} of {result.trades.length} trades profitable</p>
            </div>

            <div className="bg-white dark:bg-slate-800 p-5 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <p className="text-slate-500 text-sm font-medium">Max Drawdown</p>
                <div className="p-2 bg-orange-50 text-orange-600 rounded-lg">
                  <TrendingDown size={16} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                {result.max_drawdown.toFixed(2)}%
              </h3>
              <p className="text-xs text-slate-400 mt-1">Risk exposure during period</p>
            </div>

            <div className="bg-white dark:bg-slate-800 p-5 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm">
              <div className="flex justify-between items-start mb-2">
                <p className="text-slate-500 text-sm font-medium">Sharpe Ratio</p>
                <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                  <BarChart3 size={16} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                {result.sharpe_ratio.toFixed(2)}
              </h3>
              <p className="text-xs text-slate-400 mt-1">Risk-adjusted return metric</p>
            </div>
          </div>

          {/* Performance Chart */}
          <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
              Equity Curve
              <span className="text-xs font-normal text-slate-400 px-2 py-0.5 bg-slate-100 dark:bg-slate-700 rounded-full">Portfolio vs Price</span>
            </h3>
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={result.history}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis 
                    dataKey="date" 
                    tick={{fontSize: 10}} 
                    tickFormatter={(val) => new Date(val).toLocaleDateString()}
                    stroke="#94a3b8"
                  />
                  <YAxis 
                    yAxisId="left"
                    tick={{fontSize: 10}}
                    stroke="#94a3b8"
                    domain={['auto', 'auto']}
                    tickFormatter={(val) => `$${val.toLocaleString()}`}
                  />
                  <YAxis 
                    yAxisId="right" 
                    orientation="right" 
                    tick={{fontSize: 10}}
                    stroke="#94a3b8"
                    domain={['auto', 'auto']}
                    hide
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    labelFormatter={(label) => new Date(label).toLocaleDateString()}
                  />
                  <Legend verticalAlign="top" height={36}/>
                  <Area 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="portfolio_value" 
                    name="Portfolio Value" 
                    stroke="#3b82f6" 
                    strokeWidth={3}
                    fillOpacity={1} 
                    fill="url(#colorValue)" 
                    dot={false}
                  />
                  <Line 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="close" 
                    name="Stock Price" 
                    stroke="#94a3b8" 
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Trade Details */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-100 dark:border-slate-700 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center">
              <h3 className="text-lg font-bold">Trade Execution History</h3>
              <span className="text-xs font-medium px-2.5 py-1 bg-blue-50 text-blue-600 rounded-full">
                {result.trades.length} Transactions
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-slate-50 dark:bg-slate-900/50 text-slate-500 text-xs uppercase font-bold">
                  <tr>
                    <th className="px-6 py-4">Execution Date</th>
                    <th className="px-6 py-4">Action</th>
                    <th className="px-6 py-4">Price</th>
                    <th className="px-6 py-4">Units</th>
                    <th className="px-6 py-4">Result</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {result.trades.slice().reverse().map((trade: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-900/30 transition-colors">
                      <td className="px-6 py-4 text-sm whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <Calendar size={14} className="text-slate-400" />
                          {new Date(trade.date).toLocaleDateString()}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${trade.type === 'BUY' ? 'bg-blue-100 text-blue-600' : 'bg-orange-100 text-orange-600'}`}>
                          {trade.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm font-medium">₩{trade.price.toLocaleString()}</td>
                      <td className="px-6 py-4 text-sm text-slate-500">{trade.quantity.toLocaleString()}</td>
                      <td className="px-6 py-4">
                        {trade.profit !== undefined && (
                          <span className={`text-sm font-bold ${trade.profit >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                            {trade.profit >= 0 ? '+' : ''}{trade.profit.toLocaleString()} ({(trade.profit_pct * 100).toFixed(2)}%)
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                  {result.trades.length === 0 && (
                    <tr>
                      <td colSpan={5} className="px-6 py-10 text-center text-slate-400 italic">
                        No trades executed for this period.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {!result && !isLoading && (
        <div className="flex flex-col items-center justify-center py-20 bg-slate-50 dark:bg-slate-900/50 rounded-3xl border-2 border-dashed border-slate-200 dark:border-slate-800">
          <div className="bg-white dark:bg-slate-800 p-4 rounded-full shadow-lg mb-4 text-blue-600">
            <BarChart3 size={32} />
          </div>
          <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-2">Ready to Run Backtest</h3>
          <p className="text-slate-500 text-sm max-w-md text-center">
            Configure your parameters above and click "Run Analysis" to see how this strategy would have performed.
          </p>
        </div>
      )}
    </div>
  );
};

export default BacktestReport;
