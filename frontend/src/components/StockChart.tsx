import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, ISeriesApi, Time, CandlestickSeries, LineSeries } from 'lightweight-charts';

export interface ChartDataPoint {
  time: Time;
  open: number;
  high: number;
  low: number;
  close: number;
  tenkan_sen?: number;
  kijun_sen?: number;
  senkou_span_a?: number;
  senkou_span_b?: number;
}

interface StockChartProps {
  data: ChartDataPoint[];
  colors?: {
    upColor?: string;
    downColor?: string;
    tenkanColor?: string;
    kijunColor?: string;
    senkouAColor?: string;
    senkouBColor?: string;
    backgroundColor?: string;
    textColor?: string;
  };
}

const StockChart: React.FC<StockChartProps> = ({ data, colors }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  // Use defaults matching our UI design
  const {
    upColor = '#ef4444',     // Korean market up
    downColor = '#0ea5e9',   // Korean market down
    tenkanColor = '#f59e0b', // Amber
    kijunColor = '#8b5cf6',  // Purple
    senkouAColor = '#10b981',// Emerald
    senkouBColor = '#f43f5e',// Rose
    backgroundColor = 'transparent',
    textColor = '#64748b',   // Slate 500
  } = colors || {};

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

    // Initialize Chart
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: backgroundColor },
        textColor,
      },
      grid: {
        vertLines: { color: 'rgba(100, 116, 139, 0.1)' },
        horzLines: { color: 'rgba(100, 116, 139, 0.1)' },
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      crosshair: {
        mode: 1, // Normal crosshair
      }
    });

    // 1. Candlestick Series
    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor,
      downColor,
      borderVisible: false,
      wickUpColor: upColor,
      wickDownColor: downColor,
    });

    const candleData = data.map(d => ({
      time: d.time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));
    candleSeries.setData(candleData);

    // Helper to add line series
    const addLine = (color: string, key: keyof ChartDataPoint, lineWidth: number = 2) => {
      const lineSeries = chart.addSeries(LineSeries, {
        color,
        lineWidth: lineWidth as any,
        crosshairMarkerVisible: false,
        lastValueVisible: false,
        priceLineVisible: false,
      });

      const lineData = data
        .filter(d => d[key] !== undefined && d[key] !== null)
        .map(d => ({
          time: d.time,
          value: d[key] as number,
        }));
      
      lineSeries.setData(lineData);
      return lineSeries;
    };

    // 2. Ichimoku Lines
    addLine(tenkanColor, 'tenkan_sen', 2);
    addLine(kijunColor, 'kijun_sen', 2);
    addLine(senkouAColor, 'senkou_span_a', 1);
    addLine(senkouBColor, 'senkou_span_b', 1);

    // Fit Content
    chart.timeScale().fitContent();

    // Handle Resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, upColor, downColor, tenkanColor, kijunColor, senkouAColor, senkouBColor, backgroundColor, textColor]);

  return <div ref={chartContainerRef} className="w-full h-full min-h-[400px]" />;
};

export default StockChart;
