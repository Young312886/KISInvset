import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { cn } from "../../lib/utils";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table";
import { Badge } from "../ui/badge";
import { Progress } from "../ui/progress";

interface WatchlistItem {
  symbol: string;
  name: string;
  price: number;
  change: number;
  score: number;
  signal: string;
}

interface WatchlistTableProps {
  watchList: WatchlistItem[];
}

const PriceCell: React.FC<{ price: number }> = ({ price }) => {
  const [flashColor, setFlashColor] = useState<'text-red-500' | 'text-blue-500' | 'text-foreground'>('text-foreground');
  const prevPriceRef = useRef<number>(price);

  useEffect(() => {
    if (price !== prevPriceRef.current) {
      if (price > prevPriceRef.current) {
        setFlashColor('text-red-500'); // Korean market: red is up
      } else if (price < prevPriceRef.current) {
        setFlashColor('text-blue-500'); // Korean market: blue is down
      }
      
      const timer = setTimeout(() => {
        setFlashColor('text-foreground');
      }, 500); // flash duration
      
      prevPriceRef.current = price;
      return () => clearTimeout(timer);
    }
  }, [price]);

  return (
    <TableCell className={cn("text-right font-bold transition-colors duration-300", flashColor)}>
      ₩{price.toLocaleString()}
    </TableCell>
  );
};

const WatchlistTable: React.FC<WatchlistTableProps> = ({ watchList }) => {
  return (
    <Card className="bento-box p-0 border-none h-full">
      <CardHeader className="p-8 pb-4">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="text-2xl font-bold tracking-tight text-foreground">Watchlist</CardTitle>
            <CardDescription className="text-muted-foreground">Your prioritized stocks with Value-Trend scores</CardDescription>
          </div>
          <Button variant="link" className="text-primary font-bold hover:no-underline px-0">Manage</Button>
        </div>
      </CardHeader>
      <CardContent className="p-8 pt-0">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent border-muted/50">
              <TableHead className="font-bold text-muted-foreground uppercase tracking-widest text-[10px]">Asset</TableHead>
              <TableHead className="text-right font-bold text-muted-foreground uppercase tracking-widest text-[10px]">Price</TableHead>
              <TableHead className="text-right font-bold text-muted-foreground uppercase tracking-widest text-[10px]">Change</TableHead>
              <TableHead className="text-center font-bold text-muted-foreground uppercase tracking-widest text-[10px]">Score</TableHead>
              <TableHead className="text-center font-bold text-muted-foreground uppercase tracking-widest text-[10px]">Signal</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {watchList.map((stock) => (
              <TableRow key={stock.symbol} className="group cursor-pointer border-muted/30 hover:bg-secondary/20 transition-colors">
                <TableCell className="py-5">
                  <Link to={`/stock/${stock.symbol}`} className="flex items-center space-x-4">
                    <div className="h-12 w-12 rounded-2xl bg-secondary flex items-center justify-center font-black text-secondary-foreground shadow-inner">
                      {stock.name.charAt(0)}
                    </div>
                    <div>
                      <div className="font-bold group-hover:text-primary transition-colors text-foreground">{stock.name}</div>
                      <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-tighter">{stock.symbol}</div>
                    </div>
                  </Link>
                </TableCell>
                <PriceCell price={stock.price} />
                <TableCell className="text-right">
                  <div className={cn(
                    "text-sm font-black transition-colors duration-300",
                    stock.change > 0 ? "text-red-500" : stock.change < 0 ? "text-blue-500" : "text-foreground"
                  )}>
                    {stock.change > 0 ? '+' : ''}{stock.change}%
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <div className="flex flex-col items-center gap-1.5">
                    <span className="text-sm font-black text-foreground">{stock.score}</span>
                    <Progress value={stock.score} className="w-12 h-1.5" />
                  </div>
                </TableCell>
                <TableCell className="text-center">
                  <Badge className={cn(
                    "rounded-lg font-black tracking-widest px-3 py-1 text-[10px] uppercase border",
                    stock.signal.includes('BUY') ? "bg-red-500/10 text-red-500 border-red-500/20 shadow-[0_0_10px_rgba(239,68,68,0.1)]" :
                    stock.signal === 'SELL' ? "bg-blue-500/10 text-blue-500 border-blue-500/20 shadow-[0_0_10px_rgba(59,130,246,0.1)]" :
                    "bg-muted text-muted-foreground border-transparent"
                  )}>
                    {stock.signal}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default WatchlistTable;
