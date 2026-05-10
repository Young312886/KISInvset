import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import FundamentalRadar from '../FundamentalRadar';

interface FundamentalAnalysisProps {
  radarData: any[];
  totalScore: number;
  grade: string;
}

const FundamentalAnalysis: React.FC<FundamentalAnalysisProps> = ({ radarData, totalScore, grade }) => {
  return (
    <Card className="bento-box border-none p-0">
      <CardHeader className="p-6 pb-2">
        <CardTitle className="text-xl font-bold">Fundamental Insights</CardTitle>
      </CardHeader>
      <CardContent className="p-6 flex flex-col md:flex-row items-center gap-8">
        <div className="flex-1 w-full h-[300px] flex items-center justify-center">
          <FundamentalRadar data={radarData} color="#3b82f6" />
        </div>
        
        <div className="w-full md:w-64 space-y-6">
          <div className="p-6 rounded-3xl bg-primary/5 border border-primary/10 flex flex-col items-center justify-center text-center">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest mb-1">DART Overall Score</span>
            <div className="flex items-baseline">
              <span className="text-5xl font-black text-primary">{totalScore || '-'}</span>
              <span className="text-sm font-bold text-muted-foreground ml-1">/100</span>
            </div>
            <div className="mt-4 px-4 py-1.5 rounded-full bg-primary text-primary-foreground text-xs font-black uppercase tracking-widest shadow-lg shadow-primary/20">
              Grade: {grade || '-'}
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="text-xs font-black text-muted-foreground uppercase tracking-widest px-1">Summary</h4>
            <p className="text-sm text-muted-foreground leading-relaxed px-1">
              Solid profitability metrics balanced with moderate valuation. Safety scores remain high, providing a strong margin of safety for long-term investors.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default FundamentalAnalysis;
