import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, LineChart, Briefcase, Settings, Moon, Sun, BarChart3 } from 'lucide-react';
import { create } from 'zustand';

// Simple theme store
interface ThemeState {
  isDark: boolean;
  toggleDark: () => void;
}

export const useThemeStore = create<ThemeState>((set) => ({
  isDark: true, // Default to dark mode for premium aesthetics
  toggleDark: () => set((state) => {
    const newDark = !state.isDark;
    if (newDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    return { isDark: newDark };
  }),
}));

const Layout: React.FC = () => {
  const location = useLocation();
  const { isDark, toggleDark } = useThemeStore();

  // Ensure dark mode is applied on initial load
  React.useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Snapshot', path: '/stock/005930', icon: <LineChart size={20} /> },
    { name: 'Portfolio', path: '/portfolio', icon: <Briefcase size={20} /> },
    { name: 'Backtest', path: '/backtest', icon: <BarChart3 size={20} /> },
  ];

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 dark:bg-slate-900 transition-colors duration-300">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-slate-200 dark:border-slate-800 flex flex-col m-4 rounded-3xl">
        <div className="p-6">
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600">
            KIS Invest
          </h1>
        </div>
        <nav className="flex-1 px-4 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path.split('/')[1]));
            return (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                  isActive 
                    ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium' 
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-100'
                }`}
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-slate-200 dark:border-slate-800/50">
          <button 
            onClick={toggleDark}
            className="flex w-full items-center space-x-3 px-4 py-3 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
            <span>{isDark ? 'Light Mode' : 'Dark Mode'}</span>
          </button>
          <button className="flex w-full items-center space-x-3 px-4 py-3 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 transition-colors mt-1">
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden relative">
        {/* Top Header */}
        <header className="h-20 flex items-center justify-between px-8 z-10">
          <div className="flex-1">
            <div className="relative max-w-md glass-panel rounded-full overflow-hidden">
              <input 
                type="text" 
                placeholder="Search symbol or company (e.g., 삼성전자)..." 
                className="w-full bg-transparent border-none focus:ring-0 px-6 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400"
              />
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 p-0.5">
              <div className="h-full w-full rounded-full bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <span className="text-sm font-bold text-slate-700 dark:text-slate-300">U</span>
              </div>
            </div>
          </div>
        </header>

        {/* Scrollable Main Area */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-transparent p-6 pt-0">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
