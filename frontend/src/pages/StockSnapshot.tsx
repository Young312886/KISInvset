import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Clock, Activity, BarChart2 } from 'lucide-react';
import StockChart, { ChartDataPoint } from '../components/StockChart';

// Generate mock data for visualization
const generateMockData = (): ChartDataPoint[] => {
  const data: ChartDataPoint[] = [];
  let currentPrice = 80000;
  let time = new Date('2026-04-01').getTime() / 1000;
  
  for (let i = 0; i < 100; i++) {
    const open = currentPrice + (Math.random() * 1000 - 500);
    const high = open + Math.random() * 1000;
    const low = open - Math.random() * 1000;
    const close = low + Math.random() * (high - low);
    
    data.push({
      time: time as any,
      open,
      high,
      low,
      close,
      tenkan_sen: close + (Math.random() * 500 - 250),
      kijun_sen: close + (Math.random() * 1000 - 500),
      senkou_span_a: close - 500 + (Math.random() * 400),
      senkou_span_b: close - 1000 + (Math.random() * 300),
    });
    
    currentPrice = close;
    time += 86400; // Add 1 day
  }
  return data;
};

const StockSnapshot: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();
  const [timeframe, setTimeframe] = useState('D');
  const [mockData] = useState<ChartDataPoint[]>(generateMockData());

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 100 } }
  };

  return (
    <motion.div 
      className="p-6 max-w-7xl mx-auto space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header Section */}
      <motion.div variants={itemVariants} className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white">삼성전자</h1>
            <span className="px-2 py-1 bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded text-sm font-semibold">{symbol}</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-4xl font-bold text-slate-900 dark:text-white">₩82,300</span>
            <div className="flex flex-col">
              <span className="text-sm font-medium text-red-500 flex items-center">
                <TrendingUp size={16} className="mr-1" />
                +1,200 (+1.5%)
              </span>
              <span className="text-xs text-slate-500">As of today, 15:30 KST</span>
            </div>
          </div>
        </div>
        
        {/* Signal Badge */}
        <div className="bento-box p-4 flex items-center space-x-4">
          <div className="h-12 w-12 rounded-full bg-red-500/20 flex items-center justify-center">
            <Activity className="text-red-500" size={24} />
          </div>
          <div>
            <div className="text-sm text-slate-500 dark:text-slate-400">Current Signal</div>
            <div className="text-xl font-bold text-red-500">STRONG BUY</div>
          </div>
        </div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Chart Area */}
        <motion.div variants={itemVariants} className="lg:col-span-2 bento-box p-6 min-h-[500px] flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Technical Analysis</h2>
            <div className="flex space-x-2">
              {['15M', '1H', '4H', 'D', 'W'].map(tf => (
                <button 
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                    timeframe === tf 
                      ? 'bg-blue-500 text-white shadow-md shadow-blue-500/20' 
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex-1 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-100 dark:border-slate-800 flex items-center justify-center overflow-hidden relative">
            <div className="absolute inset-0 p-2">
              <StockChart data={mockData} />
            </div>
          </div>
        </motion.div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          {/* Ichimoku Details */}
          <motion.div variants={itemVariants} className="bento-box p-6">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Ichimoku Details</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Tenkan-sen</span>
                <span className="font-medium text-slate-900 dark:text-white">81,500</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Kijun-sen</span>
                <span className="font-medium text-slate-900 dark:text-white">80,200</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Senkou Span A</span>
                <span className="font-medium text-slate-900 dark:text-white">79,800</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Senkou Span B</span>
                <span className="font-medium text-slate-900 dark:text-white">78,500</span>
              </div>
              
              <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
                <div className="text-sm text-red-500 font-medium flex items-center">
                  <TrendingUp size={16} className="mr-2" />
                  Price above cloud (Bullish)
                </div>
              </div>
            </div>
          </motion.div>

          {/* Fundamental Score */}
          <motion.div variants={itemVariants} className="bento-box p-6">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">DART Fundamental Score</h3>
            <div className="flex items-center justify-center py-4">
              <div className="relative">
                <svg className="w-32 h-32 transform -rotate-90">
                  <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="transparent" className="text-slate-100 dark:text-slate-800" />
                  <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="transparent" strokeDasharray="351.85" strokeDashoffset="87.96" className="text-blue-500" />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center flex-col">
                  <span className="text-3xl font-bold text-slate-900 dark:text-white">75</span>
                  <span className="text-xs text-slate-500">/ 100</span>
                </div>
              </div>
            </div>
            <div className="mt-2 text-center text-sm text-slate-500 dark:text-slate-400">
              Strong profitability, moderate growth
            </div>
          </motion.div>
        </div>

      </div>
    </motion.div>
  );
};

export default StockSnapshot;
