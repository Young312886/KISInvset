import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion, Variants } from 'framer-motion';
import { TrendingUp, Activity, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { cn } from '../lib/utils';
import { Badge } from "../components/ui/badge";

// Modular Components
import TechnicalAnalysis from '../components/stock/TechnicalAnalysis';
import FundamentalAnalysis from '../components/stock/FundamentalAnalysis';

// API
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

  const radarData = fundamental ? [
    { subject: '수익성', A: fundamental.profitability_score, fullMark: 100 },
    { subject: '성장성', A: fundamental.growth_score, fullMark: 100 },
    { subject: '안전성', A: fundamental.safety_score, fullMark: 100 },
    { subject: '가치평가', A: fundamental.value_score, fullMark: 100 },
    { subject: '배당매력', A: fundamental.dividend_score, fullMark: 100 },
  ] : [];

  if (isLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 animate-spin text-primary" />
          <p className="text-sm font-bold text-muted-foreground animate-pulse uppercase tracking-widest">Loading Analytics...</p>
        </div>
      </div>
    );
  }

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants: Variants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 100 } }
  };

  return (
    <motion.div 
      className="p-6 max-w-7xl mx-auto space-y-8"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header Section */}
      <motion.div variants={itemVariants} className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <h1 className="text-4xl font-black text-foreground tracking-tight">삼성전자</h1>
            <Badge variant="outline" className="text-xs font-bold px-2 py-0.5 rounded-md border-muted-foreground/30 uppercase tracking-tighter">
              {symbol}
            </Badge>
          </div>
          <div className="flex items-center space-x-5">
            <span className="text-5xl font-black text-foreground tracking-tighter">₩82,300</span>
            <div className="flex flex-col">
              <span className="text-lg font-black text-red-500 flex items-center">
                <TrendingUp size={20} className="mr-1.5" />
                +1,200 (+1.5%)
              </span>
              <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">As of today, 15:30 KST</span>
            </div>
          </div>
        </div>
        
        {/* Signal Summary Badge */}
        <div className="bento-box p-6 flex items-center space-x-5 shadow-xl shadow-primary/5">
          <div className={cn(
            "h-14 w-14 rounded-2xl flex items-center justify-center transition-all duration-500",
            signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'bg-red-500/10 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 
            signal?.signal === 'SELL' ? 'bg-blue-500/10 text-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.2)]' : 
            'bg-muted text-muted-foreground'
          )}>
            <Activity size={28} className={cn(
              signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'animate-pulse' : ''
            )} />
          </div>
          <div>
            <div className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em] mb-1">AI Live Signal</div>
            <div className={cn(
              "text-2xl font-black tracking-tight",
              signal?.signal === 'BUY' || signal?.signal === 'STRONG BUY' ? 'text-red-500' : 
              signal?.signal === 'SELL' ? 'text-blue-500' : 'text-slate-500'
            )}>{signal?.signal || 'HOLD'}</div>
          </div>
        </div>
      </motion.div>

      {/* Main Analysis Sections */}
      <motion.div variants={itemVariants} className="space-y-8">
        <TechnicalAnalysis 
          chartData={chartData} 
          timeframe={timeframe} 
          setTimeframe={setTimeframe} 
          signalDetails={signal?.details ?? {}} 
        />
        
        <FundamentalAnalysis 
          radarData={radarData} 
          totalScore={fundamental?.total_score ?? 0} 
          grade={fundamental?.grade ?? '-'} 
        />
      </motion.div>
    </motion.div>
  );
};

export default StockSnapshot;

