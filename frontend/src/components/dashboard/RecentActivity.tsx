import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";
import { getTradeHistory, TradeEntry } from '../../api/kis';
import { ShoppingCart, Tag, ArrowUpRight, ArrowDownLeft, Clock } from 'lucide-react';

const RecentActivity: React.FC = () => {
  const [activities, setActivities] = React.useState<TradeEntry[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchActivities = async () => {
      try {
        const data = await getTradeHistory(5);
        setActivities(data);
      } catch (error) {
        console.error("Failed to fetch activities", error);
      } finally {
        setLoading(false);
      }
    };
    fetchActivities();
  }, []);

  return (
    <Card className="bento-box p-0 border-none h-full flex flex-col">
      <CardHeader className="p-8 pb-4">
        <CardTitle className="text-2xl font-bold tracking-tight text-foreground">Recent Activity</CardTitle>
        <CardDescription className="text-muted-foreground">Latest market transactions</CardDescription>
      </CardHeader>
      <CardContent className="p-8 pt-0 flex-1">
        <div className="space-y-4">
          {loading ? (
            <div className="flex items-center justify-center py-10">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : activities.length === 0 ? (
            <div className="text-center py-10 text-muted-foreground">No recent activity</div>
          ) : (
            activities.map((activity) => (
              <div key={activity.id} className="flex items-center justify-between p-4 rounded-2xl bg-secondary/20 border border-muted/10 hover:bg-secondary/30 transition-all group">
                <div className="flex items-center space-x-4">
                  <div className={`p-3 rounded-xl ${activity.trade_type === 'BUY' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-rose-500/10 text-rose-500'}`}>
                    {activity.trade_type === 'BUY' ? <ArrowUpRight size={20} /> : <ArrowDownLeft size={20} />}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors">{activity.company_name}</h4>
                    <div className="flex items-center text-[10px] text-muted-foreground font-medium uppercase tracking-wider mt-1">
                      <Clock size={10} className="mr-1" />
                      {new Date(activity.traded_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-sm font-black ${activity.trade_type === 'BUY' ? 'text-emerald-500' : 'text-rose-500'}`}>
                    {activity.trade_type === 'BUY' ? '+' : '-'}{activity.quantity} Shares
                  </div>
                  <div className="text-[11px] font-bold text-muted-foreground mt-0.5">
                    ₩{activity.price.toLocaleString()}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default RecentActivity;
