import React from 'react';
import { motion, Variants } from 'framer-motion';
import { Activity, RefreshCw, Plus } from 'lucide-react';
import { Button } from "../components/ui/button";

// Modular Dashboard Components
import KPICard from '../components/dashboard/KPICard';
import WatchlistTable from '../components/dashboard/WatchlistTable';
import SignalPanel from '../components/dashboard/SignalPanel';
import PortfolioAllocation from '../components/dashboard/PortfolioAllocation';
import MarketPulse from '../components/dashboard/MarketPulse';

const Dashboard: React.FC = () => {
  const watchList = [
    { symbol: '005930', name: '삼성전자', price: 82300, change: 1.5, score: 85, signal: 'STRONG BUY' },
    { symbol: '000660', name: 'SK하이닉스', price: 178500, change: -0.8, score: 62, signal: 'HOLD' },
    { symbol: '035420', name: 'NAVER', price: 192000, change: 2.1, score: 78, signal: 'BUY' },
    { symbol: '373220', name: 'LG에너지솔루션', price: 385000, change: -1.2, score: 45, signal: 'SELL' },
  ];

  const recentSignals = [
    { symbol: '005930', name: '삼성전자', type: '3역 호전 (Triple Bullish)', time: '10 mins ago', strength: 'Strong', color: 'red' },
    { symbol: '066570', name: 'LG전자', type: '구름대 돌파 (Kumo Breakout)', time: '45 mins ago', strength: 'Medium', color: 'blue' },
    { symbol: '035720', name: '카카오', type: '기준선 반등 (Kijun Support)', time: '2 hours ago', strength: 'Weak', color: 'purple' },
  ];

  const marketKPIs = [
    { title: 'KOSPI', value: '2,753.21', change: 1.25, data: [2710, 2725, 2720, 2740, 2735, 2753], isUp: true },
    { title: 'KOSDAQ', value: '870.45', change: -0.48, data: [880, 875, 878, 872, 874, 870], isUp: false },
    { title: 'Portfolio Value', value: '₩124.5M', change: 3.8, data: [118, 120, 119, 122, 123, 124.5], isUp: true },
    { title: 'Active Signals', value: '24', change: 12, data: [15, 18, 16, 20, 22, 24], isUp: true, isCount: true },
  ];

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants: Variants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: 'spring', stiffness: 100 }
    }
  };

  return (
    <motion.div 
      className="p-6 max-w-7xl mx-auto space-y-8"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-foreground">
            Market Dashboard
          </h1>
          <p className="text-muted-foreground mt-1 flex items-center">
            <Activity size={16} className="mr-2 text-primary" />
            AI-powered technical analysis & fundamental insights
          </p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" className="rounded-xl shadow-sm border-muted/50 hover:bg-secondary transition-colors">
            <RefreshCw size={18} className="mr-2" />
            Refresh
          </Button>
          <Button className="rounded-xl shadow-lg bg-primary hover:bg-primary/90 text-primary-foreground transition-all hover:scale-[1.02] active:scale-[0.98]">
            <Plus size={18} className="mr-2" />
            Add Asset
          </Button>
        </div>
      </div>

      {/* Market Overview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {marketKPIs.map((kpi, idx) => (
          <motion.div key={idx} variants={itemVariants}>
            <KPICard {...kpi} />
          </motion.div>
        ))}
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <motion.div variants={itemVariants} className="lg:col-span-2">
          <WatchlistTable watchList={watchList} />
        </motion.div>
        <motion.div variants={itemVariants}>
          <MarketPulse />
        </motion.div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div variants={itemVariants}>
          <SignalPanel signals={recentSignals} />
        </motion.div>
        <motion.div variants={itemVariants}>
          <PortfolioAllocation />
        </motion.div>
      </div>
    </motion.div>
  );
};



export default Dashboard;

