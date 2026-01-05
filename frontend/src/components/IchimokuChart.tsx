import { createChart, IChartApi, ISeriesApi, CandlestickData, LineData, UTCTimestamp } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react';
import { ChartData } from '../api/kis';

interface ChartProps {
    data: ChartData[];
}

const IchimokuChart: React.FC<ChartProps> = ({ data }) => {
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);

    useEffect(() => {
        if (!chartContainerRef.current || data.length === 0) return;

        // Create chart instance
        chartRef.current = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.clientWidth,
            height: 500,
            layout: { background: { color: '#ffffff' }, textColor: '#333' },
            grid: { vertLines: { color: '#e1e1e1' }, horzLines: { color: '#e1e1e1' } },
            timeScale: { timeVisible: true, secondsVisible: false },
        });

        const chart = chartRef.current;

        // Prepare data series
        const candlestickSeries = chart.addCandlestickSeries();
        const tenkanSeries = chart.addLineSeries({ color: '#007bff', lineWidth: 1 });
        const kijunSeries = chart.addLineSeries({ color: '#dc3545', lineWidth: 1 });
        const senkouASeries = chart.addLineSeries({ color: 'rgba(25, 135, 84, 0.5)', lineWidth: 1 });
        const senkouBSeries = chart.addLineSeries({ color: 'rgba(220, 53, 69, 0.5)', lineWidth: 1 });
        const chikouSeries = chart.addLineSeries({ color: '#6c757d', lineWidth: 1 });
        
        chart.addAreaSeries({
            topLineColor: 'rgba(25, 135, 84, 0.5)',
            bottomLineColor: 'rgba(220, 53, 69, 0.5)',
            topColor: 'rgba(25, 135, 84, 0.1)',
            bottomColor: 'rgba(220, 53, 69, 0.1)',
            lineWidth: 0,
        });


        // Format data for lightweight-charts
        const formatTime = (dateStr: string) => (new Date(dateStr).getTime() / 1000) as UTCTimestamp;

        const ohlcData: CandlestickData[] = data.map(d => ({
            time: formatTime(d.date),
            open: d.open,
            high: d.high,
            low: d.low,
            close: d.close,
        }));

        const tenkanData: LineData[] = data.filter(d => d.tenkan_sen).map(d => ({ time: formatTime(d.date), value: d.tenkan_sen! }));
        const kijunData: LineData[] = data.filter(d => d.kijun_sen).map(d => ({ time: formatTime(d.date), value: d.kijun_sen! }));
        const senkouAData: LineData[] = data.filter(d => d.senkou_span_a).map(d => ({ time: formatTime(d.date), value: d.senkou_span_a! }));
        const senkouBData: LineData[] = data.filter(d => d.senkou_span_b).map(d => ({ time: formatTime(d.date), value: d.senkou_span_b! }));
        const chikouData: LineData[] = data.filter(d => d.chikou_span).map(d => ({ time: formatTime(d.date), value: d.chikou_span! }));

        // Set data to series
        candlestickSeries.setData(ohlcData);
        tenkanSeries.setData(tenkanData);
        kijunSeries.setData(kijunData);
        senkouASeries.setData(senkouAData);
        senkouBSeries.setData(senkouBData);
        chikouSeries.setData(chikouData);

        chart.timeScale().fitContent();

        // Cleanup on unmount
        return () => {
            if (chart) {
                chart.remove();
                chartRef.current = null;
            }
        };
    }, [data]);

    return <div ref={chartContainerRef} className="w-full h-full" />;
};

export default IchimokuChart;
