import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import StockChart from '../StockChart';

interface TechnicalAnalysisProps {
  chartData: any;
  timeframe: string;
  setTimeframe: (tf: string) => void;
  signalDetails: any;
}

const TechnicalAnalysis: React.FC<TechnicalAnalysisProps> = ({ chartData, timeframe, setTimeframe, signalDetails }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <Card className="lg:col-span-2 bento-box border-none p-0">
        <CardHeader className="p-6 pb-2 flex flex-row items-center justify-between space-y-0">
          <CardTitle className="text-xl font-bold">Technical Analysis</CardTitle>
          <div className="flex space-x-1 bg-secondary/50 p-1 rounded-xl">
            {['15M', '1H', '4H', 'D', 'W'].map(tf => (
              <button 
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  timeframe === tf 
                    ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                    : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
        </CardHeader>
        <CardContent className="p-6 h-[450px]">
          <div className="h-full w-full bg-secondary/20 rounded-2xl border border-border/50 overflow-hidden relative">
            <div className="absolute inset-0 p-2">
              {chartData && <StockChart data={chartData} />}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="bento-box border-none p-0">
        <CardHeader className="p-6 pb-2">
          <CardTitle className="text-xl font-bold">Ichimoku Details</CardTitle>
        </CardHeader>
        <CardContent className="p-6 space-y-5">
          <div className="space-y-4">
            <div className="flex justify-between items-center group">
              <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">Tenkan-sen</span>
              <span className="font-bold text-foreground">{signalDetails?.tenkan_sen?.toLocaleString() || '-'}</span>
            </div>
            <div className="flex justify-between items-center group">
              <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">Kijun-sen</span>
              <span className="font-bold text-foreground">{signalDetails?.kijun_sen?.toLocaleString() || '-'}</span>
            </div>
            <div className="flex justify-between items-center group">
              <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">Senkou Span A</span>
              <span className="font-bold text-foreground">{signalDetails?.senkou_span_a?.toLocaleString() || '-'}</span>
            </div>
            <div className="flex justify-between items-center group">
              <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">Senkou Span B</span>
              <span className="font-bold text-foreground">{signalDetails?.senkou_span_b?.toLocaleString() || '-'}</span>
            </div>
          </div>
          
          <div className="pt-6 border-t border-border/50">
            <div className="p-4 rounded-2xl bg-red-500/5 border border-red-500/10">
              <div className="text-xs font-black text-red-500 flex items-center uppercase tracking-widest">
                <TrendingUp size={14} className="mr-2" />
                Signal Insight
              </div>
              <p className="mt-2 text-sm font-medium text-muted-foreground leading-relaxed">
                Price is currently <span className="text-red-500 font-bold">above the cloud</span>, indicating a strong bullish trend on the daily timeframe.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default TechnicalAnalysis;
