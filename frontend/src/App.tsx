import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from './pages/Dashboard';
import StockSnapshot from './pages/StockSnapshot';
import Portfolio from './pages/Portfolio';
import BacktestReport from './pages/BacktestReport';
import Layout from './components/Layout';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 60 * 1000, // 1 minute
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="dark:bg-slate-900 min-h-screen text-slate-900 dark:text-slate-100 transition-colors duration-300">
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="stock/:symbol" element={<StockSnapshot />} />
              <Route path="portfolio" element={<Portfolio />} />
              <Route path="backtest" element={<BacktestReport />} />
              {/* Other routes will be added here */}
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
