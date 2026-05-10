import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Activity, AlertCircle, RefreshCw } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  // Mock data for initial UI dev
  const watchList = [
    { symbol: '005930', name: '삼성전자', price: 82300, change: 1.5, signal: 'BUY' },
    { symbol: '000660', name: 'SK하이닉스', price: 178500, change: -0.8, signal: 'HOLD' },
    { symbol: '035420', name: 'NAVER', price: 192000, change: 2.1, signal: 'BUY' },
    { symbol: '373220', name: 'LG에너지솔루션', price: 385000, change: -1.2, signal: 'SELL' },
  ];

  const recentSignals = [
    { symbol: '005930', name: '삼성전자', type: 'Golden Cross', time: '10 mins ago', strength: 'Strong' },
    { symbol: '000660', name: 'SK하이닉스', type: 'Kumo Breakout', time: '1 hour ago', strength: 'Medium' },
    { symbol: '035420', name: 'NAVER', type: 'Tenkan/Kijun Cross', time: '2 hours ago', strength: 'Weak' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: 'spring', stiffness: 100 }
    }
  };

  return (
    <motion.div 
      className="p-6 max-w-7xl mx-auto space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Market Overview</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Today's technical signals and portfolio metrics</p>
        </div>
        <button className="flex items-center space-x-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 px-4 py-2 rounded-xl hover:opacity-90 transition-opacity font-medium">
          <RefreshCw size={18} />
          <span>Sync Data</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { title: 'KOSPI', value: '2,753.21', change: 1.2, isUp: true },
          { title: 'KOSDAQ', value: '870.45', change: -0.5, isUp: false },
          { title: 'Active Signals', value: '14', text: '5 Strong Buys', isNeutral: true },
        ].map((kpi, idx) => (
          <motion.div key={idx} variants={itemVariants} className="bento-box p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 dark:bg-blue-400/5 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-blue-500/10 transition-colors"></div>
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">{kpi.title}</h3>
            <div className="mt-2 flex items-baseline space-x-2">
              <span className="text-3xl font-bold text-slate-900 dark:text-white">{kpi.value}</span>
            </div>
            {!kpi.isNeutral && (
              <div className={`mt-4 flex items-center text-sm font-medium ${kpi.isUp ? 'text-red-500' : 'text-blue-500'}`}>
                {kpi.isUp ? <TrendingUp size={16} className="mr-1" /> : <TrendingDown size={16} className="mr-1" />}
                {kpi.change}% from yesterday
              </div>
            )}
            {kpi.isNeutral && (
              <div className="mt-4 flex items-center text-sm font-medium text-purple-500">
                <Activity size={16} className="mr-1" />
                {kpi.text}
              </div>
            )}
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Watchlist */}
        <motion.div variants={itemVariants} className="lg:col-span-2 bento-box p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Watchlist</h2>
            <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">View All</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  <th className="pb-4">Asset</th>
                  <th className="pb-4">Price</th>
                  <th className="pb-4">24h Change</th>
                  <th className="pb-4">Signal</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
                {watchList.map((stock) => (
                  <tr key={stock.symbol} className="group hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors cursor-pointer">
                    <td className="py-4">
                      <Link to={`/stock/${stock.symbol}`} className="flex items-center space-x-3">
                        <div className="h-10 w-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-bold text-slate-700 dark:text-slate-300">
                          {stock.name.charAt(0)}
                        </div>
                        <div>
                          <div className="font-semibold text-slate-900 dark:text-white">{stock.name}</div>
                          <div className="text-xs text-slate-500">{stock.symbol}</div>
                        </div>
                      </Link>
                    </td>
                    <td className="py-4 font-medium text-slate-900 dark:text-white">
                      ₩{stock.price.toLocaleString()}
                    </td>
                    <td className="py-4">
                      <div className={`flex items-center text-sm font-medium ${stock.change > 0 ? 'text-red-500' : 'text-blue-500'}`}>
                        {stock.change > 0 ? <TrendingUp size={16} className="mr-1" /> : <TrendingDown size={16} className="mr-1" />}
                        {Math.abs(stock.change)}%
                      </div>
                    </td>
                    <td className="py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        stock.signal === 'BUY' ? 'bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400' :
                        stock.signal === 'SELL' ? 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400' :
                        'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400'
                      }`}>
                        {stock.signal}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Recent Signals */}
        <motion.div variants={itemVariants} className="bento-box p-6 flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Live Signals</h2>
            <AlertCircle size={20} className="text-slate-400" />
          </div>
          <div className="flex-1 space-y-4">
            {recentSignals.map((signal, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 hover:border-blue-200 dark:hover:border-blue-500/30 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <div className="font-semibold text-slate-900 dark:text-white">{signal.name}</div>
                  <span className="text-xs text-slate-500">{signal.time}</span>
                </div>
                <div className="text-sm font-medium bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 mb-2">
                  {signal.type}
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-slate-500">Strength:</span>
                  <div className="flex-1 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full ${
                        signal.strength === 'Strong' ? 'bg-red-500 w-full' :
                        signal.strength === 'Medium' ? 'bg-yellow-500 w-2/3' : 'bg-blue-500 w-1/3'
                      }`}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-4 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
            View Signal History
          </button>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Dashboard;
