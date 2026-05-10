import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Progress } from "../ui/progress";
import { TrendingUp, TrendingDown, Info } from 'lucide-react';

const MarketPulse: React.FC = () => {
  return (
    <Card className="bento-box p-0 border-none">
      <CardHeader className="p-6 pb-2 flex flex-row items-center justify-between">
        <CardTitle className="text-lg font-bold text-foreground">Market Pulse</CardTitle>
        <Info size={16} className="text-muted-foreground cursor-help" />
      </CardHeader>
      <CardContent className="p-6 pt-2">
        <div className="flex justify-between items-end mb-4">
          <div className="flex flex-col">
            <span className="text-3xl font-black text-red-500 flex items-center">
              68% <TrendingUp size={24} className="ml-2" />
            </span>
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Bullish Sentiment</span>
          </div>
          <div className="text-right">
            <span className="text-xl font-bold text-foreground italic">Greed</span>
            <div className="text-[10px] text-muted-foreground">Market Mood</div>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="relative pt-2">
            <div className="flex justify-between text-[10px] font-black uppercase tracking-tighter mb-1">
              <span className="text-blue-500">Extreme Fear</span>
              <span className="text-red-500">Extreme Greed</span>
            </div>
            <Progress value={68} className="h-3 bg-secondary/50" />
            <div className="absolute top-1/2 left-[68%] -translate-y-1/2 w-1 h-5 bg-foreground rounded-full shadow-lg border-2 border-background z-10"></div>
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2">
            <div className="p-3 rounded-2xl bg-red-500/10 border border-red-500/20">
              <div className="text-[10px] font-bold text-red-500 uppercase">Advancing</div>
              <div className="text-lg font-black">1,420</div>
            </div>
            <div className="p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20">
              <div className="text-[10px] font-bold text-blue-500 uppercase">Declining</div>
              <div className="text-lg font-black">845</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default MarketPulse;
