import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { cn } from "../../lib/utils";
import { Card, CardContent } from "../ui/card";
import Sparkline from './Sparkline';

interface KPICardProps {
  title: string;
  value: string;
  change: number;
  data: number[];
  isUp: boolean;
  isCount?: boolean;
}

const KPICard: React.FC<KPICardProps> = ({ title, value, change, data, isUp, isCount }) => {
  return (
    <Card className="bento-box p-0 border-none">
      <CardContent className="p-6 relative">
        <div className={cn(
          "absolute top-0 right-0 w-24 h-24 rounded-full blur-3xl -mr-12 -mt-12 opacity-20",
          isUp ? "bg-red-500" : "bg-blue-500"
        )}></div>
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">{title}</h3>
            <div className="mt-1 text-2xl font-black">{value}</div>
          </div>
          <Sparkline data={data} color={isUp ? '#ef4444' : '#3b82f6'} />
        </div>
        <div className={cn(
          "mt-4 flex items-center text-sm font-bold",
          isUp ? "text-red-500" : "text-blue-500"
        )}>
          {isUp ? <ArrowUpRight size={16} className="mr-1" /> : <ArrowDownRight size={16} className="mr-1" />}
          {Math.abs(change)}{isCount ? ' new' : '%'}
          <span className="ml-2 text-xs font-medium text-muted-foreground">vs yesterday</span>
        </div>
      </CardContent>
    </Card>
  );
};

export default KPICard;
