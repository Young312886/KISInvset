import React from 'react';
import { cn } from "../../lib/utils";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";

interface Signal {
  symbol: string;
  name: string;
  type: string;
  time: string;
  strength: string;
  color: string;
}

interface SignalPanelProps {
  signals: Signal[];
}

const SignalPanel: React.FC<SignalPanelProps> = ({ signals }) => {
  return (
    <Card className="bento-box p-0 border-none h-full flex flex-col">
      <CardHeader className="p-8 pb-4">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="text-2xl font-bold tracking-tight text-foreground">Live Signals</CardTitle>
            <CardDescription className="text-muted-foreground">Real-time technical alerts</CardDescription>
          </div>
          <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]"></div>
        </div>
      </CardHeader>
      <CardContent className="p-8 pt-0 flex-1 space-y-4 overflow-y-auto custom-scrollbar">
        {signals.map((signal, idx) => (
          <div 
            key={idx} 
            className="group p-5 rounded-3xl bg-secondary/30 border border-transparent hover:border-primary/30 hover:bg-secondary/50 transition-all duration-300"
          >
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center space-x-3">
                <div className={cn(
                  "h-2 w-2 rounded-full shadow-sm",
                  signal.color === 'red' ? 'bg-red-500 shadow-red-500/50' : 
                  signal.color === 'blue' ? 'bg-blue-500 shadow-blue-500/50' : 
                  'bg-purple-500 shadow-purple-500/50'
                )}></div>
                <span className="font-bold text-foreground group-hover:text-primary transition-colors">{signal.name}</span>
              </div>
              <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">{signal.time}</span>
            </div>
            
            <div className={cn(
              "text-sm font-black mb-4",
              signal.color === 'red' ? 'text-red-500' : 
              signal.color === 'blue' ? 'text-blue-500' : 
              'text-purple-600 dark:text-purple-400'
            )}>
              {signal.type}
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Strength</span>
                <div className="flex space-x-1">
                  {[1, 2, 3].map((step) => (
                    <div 
                      key={step}
                      className={cn(
                        "h-1.5 w-4 rounded-full transition-all duration-500",
                        (signal.strength === 'Strong' || (signal.strength === 'Medium' && step <= 2) || (signal.strength === 'Weak' && step === 1)) 
                        ? (signal.color === 'red' ? 'bg-red-500' : signal.color === 'blue' ? 'bg-blue-500' : 'bg-purple-500') 
                        : "bg-muted/50"
                      )}
                    ></div>
                  ))}
                </div>
              </div>
              <Button variant="ghost" size="sm" className="h-7 px-3 text-[10px] font-black uppercase tracking-tighter opacity-0 group-hover:opacity-100 transition-all transform translate-y-1 group-hover:translate-y-0">
                Analyze
              </Button>
            </div>
          </div>
        ))}
      </CardContent>
      <div className="p-8 pt-4">
        <Button className="w-full h-12 rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg hover:shadow-primary/20 transition-all bg-primary hover:bg-primary/90 text-primary-foreground">
          Open Signals Panel
        </Button>
      </div>
    </Card>
  );
};

export default SignalPanel;
