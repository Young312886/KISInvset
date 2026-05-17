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
import RecentActivity from '../components/dashboard/RecentActivity';

import { getWatchlist, getFundamentalScore, getMultiplePrices, getMarketIndices, getPortfolioAssets, WatchlistItem, SignalData, StockPrice, PortfolioAsset } from '../api/kis';
import { Skeleton } from "../components/ui/skeleton";
import { useWebSocket } from '../hooks/useWebSocket';
import { useMarketStore } from '../store/marketStore';

const Dashboard: React.FC = () => {
  const [watchList, setWatchList] = React.useState<any[]>([]);
  const [marketKPIs, setMarketKPIs] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState({
    watchlist: true,
    market: true,
    portfolio: true
  });

  const { subscribe } = useWebSocket();
  const realtimePrices = useMarketStore(state => state.realtimePrices);

  const fetchData = async () => {
    // 1. Fetch Market Indices first for KPIs
    getMarketIndices().then(indices => {
      setMarketKPIs(prev => {
        const updated = [...prev];
        // KOSPI
        updated[0] = { 
          title: 'KOSPI', 
          value: indices.KOSPI?.current_price?.toLocaleString() || '---', 
          change: indices.KOSPI?.change_rate || 0, 
          data: [2710, 2725, 2720, 2740, 2735, indices.KOSPI?.current_price || 2735], 
          isUp: (indices.KOSPI?.change || 0) > 0 
        };
        // KOSDAQ
        updated[1] = { 
          title: 'KOSDAQ', 
          value: indices.KOSDAQ?.current_price?.toLocaleString() || '---', 
          change: indices.KOSDAQ?.change_rate || 0, 
          data: [880, 875, 878, 872, 874, indices.KOSDAQ?.current_price || 874], 
          isUp: (indices.KOSDAQ?.change || 0) > 0 
        };
        return updated;
      });
      setLoading(prev => ({ ...prev, market: false }));
    });

    // 2. Fetch Watchlist and then enrich with prices/scores
    getWatchlist().then(async (watchlistItems) => {
      const symbols = watchlistItems.map(item => item.symbol);
      
      // Fetch prices and fundamental scores in parallel
      const [prices, scores] = await Promise.all([
        getMultiplePrices(symbols).catch(() => ({})),
        Promise.all(symbols.map(s => getFundamentalScore(s).catch(() => null)))
      ]);

      const enhancedItems = watchlistItems.map((item, idx) => {
        const priceData = prices[item.symbol];
        const scoreData = scores[idx];
        
        // Subscribe to real-time price updates
        subscribe(item.symbol);
        
        return {
          symbol: item.symbol,
          name: item.company_name,
          price: priceData?.current_price || 0,
          change: priceData?.change_rate || 0,
          score: scoreData?.total_score || 0,
          signal: scoreData?.grade || 'N/A'
        };
      });
      
      setWatchList(enhancedItems);
      setLoading(prev => ({ ...prev, watchlist: false }));
    });

    // 3. Fetch Portfolio
    getPortfolioAssets(1).catch(() => []).then(assets => {
      const totalValue = (assets as PortfolioAsset[]).reduce((sum: number, asset: PortfolioAsset) => 
        sum + (asset.quantity * (asset.current_price || asset.avg_purchase_price)), 0
      );
      
      setMarketKPIs(prev => {
        const updated = [...prev];
        updated[2] = { 
          title: 'Portfolio Value', 
          value: `₩${(totalValue / 10000).toFixed(1)}M`, 
          change: 3.8,
          data: [118, 120, 119, 122, 123, totalValue / 10000], 
          isUp: true 
        };
        updated[3] = { 
          title: 'Active Signals', 
          value: '24', 
          change: 12, 
          data: [15, 18, 16, 20, 22, 24], 
          isUp: true, 
          isCount: true 
        };
        return updated;
      });
      setLoading(prev => ({ ...prev, portfolio: false }));
    });
  };

  React.useEffect(() => {
    fetchData();
  }, []);


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
          <Button 
            variant="outline" 
            className="rounded-xl shadow-sm border-muted/50 hover:bg-secondary transition-colors"
            onClick={fetchData}
            disabled={Object.values(loading).some(v => v)}
          >
            <RefreshCw size={18} className={`mr-2 ${Object.values(loading).some(v => v) ? 'animate-spin' : ''}`} />
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
        {loading.market ? (
          Array(4).fill(0).map((_, i) => (
            <Skeleton key={i} className="h-32 rounded-3xl" />
          ))
        ) : (
          marketKPIs.map((kpi, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <KPICard {...kpi} />
            </motion.div>
          ))
        )}
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <motion.div variants={itemVariants} className="lg:col-span-2">
          {loading.watchlist ? (
            <div className="space-y-4">
              <Skeleton className="h-8 w-48" />
              <Skeleton className="h-[400px] rounded-3xl" />
            </div>
          ) : (
            <WatchlistTable 
              watchList={watchList.map(item => ({
                ...item,
                price: realtimePrices[item.symbol]?.price || item.price,
                change: realtimePrices[item.symbol]?.change_rate || item.change
              }))} 
            />
          )}
        </motion.div>
        <motion.div variants={itemVariants}>
          <RecentActivity />
        </motion.div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div variants={itemVariants}>
          <SignalPanel signals={recentSignals} />
        </motion.div>
        <motion.div variants={itemVariants}>
          {loading.portfolio ? (
            <Skeleton className="h-[300px] rounded-3xl" />
          ) : (
            <PortfolioAllocation />
          )}
        </motion.div>
      </div>
    </motion.div>
  );
};



export default Dashboard;

