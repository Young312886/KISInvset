import React from 'react';
import { motion } from 'framer-motion';
import { Briefcase, TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight, MoreHorizontal, History, PieChart as PieChartIcon } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { getPortfolioAssets, getTradeHistory, PortfolioAsset, TradeEntry } from '../api/kis';
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Skeleton } from "../components/ui/skeleton";
import { Badge } from "../components/ui/badge";
import { cn } from "../lib/utils";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#f59e0b', '#10b981', '#06b6d4'];

const Portfolio: React.FC = () => {
  const { data: assets, isLoading: assetsLoading } = useQuery({
    queryKey: ['portfolio', 1],
    queryFn: () => getPortfolioAssets(1)
  });

  const { data: history, isLoading: historyLoading } = useQuery({
    queryKey: ['tradeHistory'],
    queryFn: () => getTradeHistory(10)
  });

  const totalValue = assets?.reduce((acc, curr) => acc + (curr.quantity * (curr.current_price || curr.avg_purchase_price)), 0) || 0;
  const totalPnL = assets?.reduce((acc, curr) => acc + curr.pnl_amount, 0) || 0;
  const pnlRate = totalValue > 0 ? (totalPnL / (totalValue - totalPnL)) * 100 : 0;

  const allocationData = assets?.map(asset => ({
    name: asset.company_name,
    value: asset.quantity * (asset.current_price || asset.avg_purchase_price)
  })).sort((a, b) => b.value - a.value) || [];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black tracking-tight">Portfolio</h1>
          <p className="text-muted-foreground mt-1">Manage your assets and track performance</p>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bento-box bg-gradient-to-br from-indigo-500/10 to-transparent border-indigo-500/20">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-bold text-muted-foreground uppercase tracking-widest">Total Value</CardTitle>
          </CardHeader>
          <CardContent>
            {assetsLoading ? <Skeleton className="h-9 w-32" /> : (
              <div className="text-3xl font-black">₩{totalValue.toLocaleString()}</div>
            )}
          </CardContent>
        </Card>
        
        <Card className="bento-box bg-gradient-to-br from-red-500/10 to-transparent border-red-500/20">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-bold text-muted-foreground uppercase tracking-widest">Total P&L</CardTitle>
          </CardHeader>
          <CardContent>
            {assetsLoading ? <Skeleton className="h-9 w-32" /> : (
              <div className={cn("text-3xl font-black flex items-center", totalPnL >= 0 ? "text-red-500" : "text-blue-500")}>
                {totalPnL >= 0 ? <ArrowUpRight className="mr-2" /> : <ArrowDownRight className="mr-2" />}
                ₩{Math.abs(totalPnL).toLocaleString()}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bento-box bg-gradient-to-br from-emerald-500/10 to-transparent border-emerald-500/20">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-bold text-muted-foreground uppercase tracking-widest">Return Rate</CardTitle>
          </CardHeader>
          <CardContent>
            {assetsLoading ? <Skeleton className="h-9 w-24" /> : (
              <div className={cn("text-3xl font-black", pnlRate >= 0 ? "text-red-500" : "text-blue-500")}>
                {pnlRate > 0 ? '+' : ''}{pnlRate.toFixed(2)}%
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Asset List */}
        <Card className="lg:col-span-2 bento-box border-none shadow-xl overflow-hidden">
          <CardHeader className="p-6 bg-secondary/30">
            <CardTitle className="text-lg font-bold flex items-center">
              <Briefcase size={20} className="mr-2 text-primary" />
              Holdings
            </CardTitle>
          </CardHeader>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase tracking-widest text-muted-foreground font-black">
                  <th className="px-6 py-4">Asset</th>
                  <th className="px-6 py-4">Quantity</th>
                  <th className="px-6 py-4">Avg. Price</th>
                  <th className="px-6 py-4">Current Price</th>
                  <th className="px-6 py-4 font-right text-right">Profit/Loss</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
                {assetsLoading ? (
                  Array(5).fill(0).map((_, i) => (
                    <tr key={i}>
                      <td className="px-6 py-4"><Skeleton className="h-10 w-32" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-16" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-24" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-24" /></td>
                      <td className="px-6 py-4 text-right"><Skeleton className="h-6 w-24 ml-auto" /></td>
                    </tr>
                  ))
                ) : assets?.map((asset) => (
                  <tr key={asset.id} className="group hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-bold text-foreground">{asset.company_name}</span>
                        <span className="text-[10px] font-medium text-muted-foreground tracking-tighter uppercase">{asset.symbol}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 font-medium">{asset.quantity.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-muted-foreground">₩{asset.avg_purchase_price.toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold">₩{(asset.current_price || asset.avg_purchase_price).toLocaleString()}</td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex flex-col items-end">
                        <span className={cn("font-black", asset.pnl_amount >= 0 ? "text-red-500" : "text-blue-500")}>
                          {asset.pnl_amount >= 0 ? '+' : ''}₩{asset.pnl_amount.toLocaleString()}
                        </span>
                        <Badge variant="outline" className={cn(
                          "w-fit text-[10px] px-1 py-0 mt-1",
                          asset.pnl_rate >= 0 ? "border-red-500/30 text-red-500 bg-red-500/5" : "border-blue-500/30 text-blue-500 bg-blue-500/5"
                        )}>
                          {asset.pnl_rate >= 0 ? '+' : ''}{asset.pnl_rate.toFixed(2)}%
                        </Badge>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Allocation Chart */}
        <Card className="bento-box border-none shadow-xl flex flex-col">
          <CardHeader className="p-6 bg-secondary/30">
            <CardTitle className="text-lg font-bold flex items-center">
              <PieChartIcon size={20} className="mr-2 text-primary" />
              Allocation
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 min-h-[300px] pt-6">
            {assetsLoading ? <Skeleton className="h-full w-full" /> : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={allocationData}
                    cx="50%"
                    cy="45%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {allocationData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip 
                    formatter={(value: number) => `₩${value.toLocaleString()}`}
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                  />
                  <Legend verticalAlign="bottom" height={36}/>
                </PieChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Trade History */}
      <Card className="bento-box border-none shadow-xl overflow-hidden">
        <CardHeader className="p-6 bg-secondary/30 flex flex-row items-center justify-between">
          <CardTitle className="text-lg font-bold flex items-center">
            <History size={20} className="mr-2 text-primary" />
            Recent Activity
          </CardTitle>
          <Badge variant="secondary" className="font-bold">Last 10 trades</Badge>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase tracking-widest text-muted-foreground font-black">
                  <th className="px-6 py-4">Type</th>
                  <th className="px-6 py-4">Asset</th>
                  <th className="px-6 py-4">Quantity</th>
                  <th className="px-6 py-4">Price</th>
                  <th className="px-6 py-4">Total</th>
                  <th className="px-6 py-4 text-right">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/50">
                {historyLoading ? (
                  Array(3).fill(0).map((_, i) => (
                    <tr key={i}>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-16" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-32" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-12" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-24" /></td>
                      <td className="px-6 py-4"><Skeleton className="h-6 w-24" /></td>
                      <td className="px-6 py-4 text-right"><Skeleton className="h-6 w-24 ml-auto" /></td>
                    </tr>
                  ))
                ) : history?.map((trade) => (
                  <tr key={trade.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4">
                      <Badge className={cn(
                        "font-black text-[10px] tracking-widest px-2 py-0.5",
                        trade.trade_type === 'BUY' ? "bg-red-500/10 text-red-500 border-red-500/20" : "bg-blue-500/10 text-blue-500 border-blue-500/20"
                      )} variant="outline">
                        {trade.trade_type}
                      </Badge>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-bold">{trade.company_name}</span>
                        <span className="text-[10px] text-muted-foreground uppercase">{trade.symbol}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 font-medium">{trade.quantity.toLocaleString()}</td>
                    <td className="px-6 py-4 font-medium text-muted-foreground">₩{trade.price.toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold text-foreground">₩{(trade.price * trade.quantity).toLocaleString()}</td>
                    <td className="px-6 py-4 text-right text-xs text-muted-foreground font-medium">
                      {new Date(trade.traded_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Portfolio;
