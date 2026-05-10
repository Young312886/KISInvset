import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Clock, Activity, BarChart2, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import StockChart, { ChartDataPoint } from '../components/StockChart';
import FundamentalRadar, { FundamentalDataPoint } from '../components/FundamentalRadar';
import { getChartData, getFundamentalScore, generateSignal } from '../api/kis';



const StockSnapshot: React.FC = () => {
  const { symbol = '005930' } = useParams<{ symbol: string }>();
  const [timeframe, setTimeframe] = useState('D');

  const { data: chartData, isLoading: isLoadingChart } = useQuery({
    queryKey: ['chart', symbol, timeframe],
    queryFn: () => getChartData(symbol, timeframe)
  });

  const { data: signal, isLoading: isLoadingSignal } = useQuery({
    queryKey: ['signal', symbol, timeframe],
    queryFn: () => generateSignal(symbol)
  });

  const { data: fundamental, isLoading: isLoadingFundamental } = useQuery({
    queryKey: ['fundamental', symbol],
    queryFn: () => getFundamentalScore(symbol)
  });

  const isLoading = isLoadingChart || isLoadingSignal || isLoadingFundamental;

  const radarData: FundamentalDataPoint[] = fundamental ? [
    { subject: '수익성', A: fundamental.profitability_score, fullMark: 100 },
    { subject: '성장성', A: fundamental.growth_score, fullMark: 100 },
    { subject: '안전성', A: fundamental.safety_score, fullMark: 100 },
    { subject: '가치평가', A: fundamental.value_score, fullMark: 100 },
    { subject: '배당매력', A: fundamental.dividend_score, fullMark: 100 },
  ] : [];

  if (isLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="w-12 h-12 animate-spin text-blue-500" />
      </div>
    );
  }

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
          <div className={`h-12 w-12 rounded-full flex items-center justify-center ${
            signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'bg-red-500/20' : 
            signal?.signal === 'SELL' ? 'bg-blue-500/20' : 'bg-slate-500/20'
          }`}>
            <Activity className={
              signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'text-red-500' : 
              signal?.signal === 'SELL' ? 'text-blue-500' : 'text-slate-500'
            } size={24} />
          </div>
          <div>
            <div className="text-sm text-slate-500 dark:text-slate-400">Current Signal</div>
            <div className={`text-xl font-bold ${
              signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'text-red-500' : 
              signal?.signal === 'SELL' ? 'text-blue-500' : 'text-slate-500'
            }`}>{signal?.signal || 'HOLD'}</div>
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
              {chartData && <StockChart data={chartData as any} />}
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
                <span className="font-medium text-slate-900 dark:text-white">{signal?.details?.tenkan_sen?.toLocaleString() || '-'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Kijun-sen</span>
                <span className="font-medium text-slate-900 dark:text-white">{signal?.details?.kijun_sen?.toLocaleString() || '-'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Senkou Span A</span>
                <span className="font-medium text-slate-900 dark:text-white">{signal?.details?.senkou_span_a?.toLocaleString() || '-'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400">Senkou Span B</span>
                <span className="font-medium text-slate-900 dark:text-white">{signal?.details?.senkou_span_b?.toLocaleString() || '-'}</span>
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
          <motion.div variants={itemVariants} className="bento-box p-6 flex flex-col items-center">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 self-start">DART Fundamental Score</h3>
            <div className="flex items-center justify-center py-4 w-full h-[250px]">
              <FundamentalRadar data={radarData} color="#3b82f6" />
            </div>
            <div className="flex items-center space-x-4 mt-2">
              <div className="text-center">
                <span className="text-3xl font-bold text-blue-500">{fundamental?.total_score || '-'}</span>
                <span className="text-sm text-slate-500">/ 100</span>
              </div>
              <div className="text-sm text-slate-500 dark:text-slate-400">
                Grade: <span className="font-bold text-slate-900 dark:text-white">{fundamental?.grade || '-'}</span>
              </div>
            </div>
          </motion.div>
        </div>

      </div>
    </motion.div>
  );
};

export default StockSnapshot;
