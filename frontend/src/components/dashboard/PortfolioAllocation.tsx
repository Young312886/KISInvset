import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";

const data = [
  { name: 'Samsung Electronics', value: 45, color: '#ef4444' },
  { name: 'SK Hynix', value: 25, color: '#f97316' },
  { name: 'NAVER', value: 15, color: '#22c55e' },
  { name: 'Cash', value: 15, color: '#94a3b8' },
];

const PortfolioAllocation: React.FC = () => {
  return (
    <Card className="bento-box p-0 border-none h-full flex flex-col">
      <CardHeader className="p-8 pb-4">
        <CardTitle className="text-2xl font-bold tracking-tight text-foreground">Portfolio Allocation</CardTitle>
        <CardDescription className="text-muted-foreground">Asset distribution by value</CardDescription>
      </CardHeader>
      <CardContent className="p-8 pt-0 flex-1 flex flex-col items-center justify-center">
        <div className="w-full h-[240px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                  borderRadius: '12px', 
                  border: 'none', 
                  color: '#fff',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' 
                }}
                itemStyle={{ color: '#fff' }}
              />
              <Legend 
                verticalAlign="bottom" 
                height={36} 
                iconType="circle"
                formatter={(value) => <span className="text-xs font-bold text-muted-foreground ml-1">{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 w-full space-y-3">
          <div className="flex justify-between items-center p-3 rounded-2xl bg-secondary/30 border border-muted/20">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Total Value</span>
            <span className="text-lg font-black text-foreground">₩124,500,000</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PortfolioAllocation;
