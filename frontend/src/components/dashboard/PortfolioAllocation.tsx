import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";

import { getPortfolioAssets, PortfolioAsset } from '../../api/kis';

const COLORS = ['#ef4444', '#f97316', '#22c55e', '#3b82f6', '#8b5cf6', '#94a3b8'];

const PortfolioAllocation: React.FC = () => {
  const [data, setData] = React.useState<any[]>([]);
  const [totalValue, setTotalValue] = React.useState(0);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const assets = await getPortfolioAssets(1); // Hardcoded account ID
        let total = 0;
        const processedData = assets.map((asset, idx) => {
          const value = asset.quantity * (asset.current_price || asset.avg_purchase_price);
          total += value;
          return {
            name: asset.company_name,
            value: value,
            color: COLORS[idx % COLORS.length]
          };
        });
        
        // Convert value to percentage for the pie chart display if needed, 
        // but Recharts handles raw values fine.
        setData(processedData);
        setTotalValue(total);
      } catch (error) {
        console.error("Failed to fetch portfolio data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
                formatter={(value: any) => `₩${Number(value).toLocaleString()}`}
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
            <span className="text-lg font-black text-foreground">₩{totalValue.toLocaleString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PortfolioAllocation;
