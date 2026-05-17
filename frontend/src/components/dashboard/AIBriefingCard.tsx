import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Sparkles, TrendingUp, AlertTriangle } from 'lucide-react';
import { getAIBriefing, AIBriefingResponse } from '../../api/ai';
import { Skeleton } from "../ui/skeleton";

interface AIBriefingCardProps {
  symbol?: string; // If not provided, we can use a top pick
}

const AIBriefingCard: React.FC<AIBriefingCardProps> = ({ symbol = '005930' }) => {
  const [briefing, setBriefing] = useState<AIBriefingResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBriefing = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getAIBriefing(symbol);
        setBriefing(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load AI Briefing');
      } finally {
        setLoading(false);
      }
    };
    
    fetchBriefing();
  }, [symbol]);

  return (
    <Card className="rounded-3xl border-0 shadow-xl bg-gradient-to-br from-card to-card/50 backdrop-blur-xl h-full flex flex-col relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
      
      <CardHeader className="pb-4 relative z-10">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-primary animate-pulse" />
            AI Insights
            <span className="text-xs font-normal px-2 py-1 bg-primary/10 text-primary rounded-full ml-2">
              Beta
            </span>
          </CardTitle>
          {briefing && (
            <div className="text-sm font-medium px-3 py-1 bg-secondary/50 rounded-full text-foreground/80">
              {symbol}
            </div>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="flex-1 relative z-10 space-y-4">
        {loading ? (
          <div className="space-y-3">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
            <div className="h-4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-32 text-destructive gap-2">
            <AlertTriangle className="w-5 h-5" />
            <p className="text-sm">{error}</p>
          </div>
        ) : briefing ? (
          <div className="space-y-4">
            <div className="prose prose-sm dark:prose-invert max-w-none text-muted-foreground leading-relaxed whitespace-pre-wrap">
              {briefing.briefing}
            </div>
            
            <div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-border/50">
              <div className="bg-secondary/30 p-3 rounded-2xl">
                <p className="text-xs text-muted-foreground mb-1 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  Recommended Weight
                </p>
                <p className="text-lg font-bold text-foreground">
                  {briefing.context_used.recommended_weight.toFixed(1)}%
                </p>
              </div>
              <div className="bg-secondary/30 p-3 rounded-2xl">
                <p className="text-xs text-muted-foreground mb-1">Market Regime</p>
                <p className="text-lg font-bold text-foreground">
                  {briefing.context_used.regime}
                </p>
              </div>
            </div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
};

export default AIBriefingCard;
