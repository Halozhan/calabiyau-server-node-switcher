import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

const LatencyChart = ({ data, title, region, serverAddr, compact = false }) => {
  const [chartData, setChartData] = useState([]);
  const [trend, setTrend] = useState("stable");

  useEffect(() => {
    if (!data || !Array.isArray(data)) return;

    // 최근 20개 데이터 포인트만 사용
    const recentData = data.slice(-20).map((item, index) => ({
      time: new Date(item.timestamp * 1000).toLocaleTimeString("ko-KR", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }),
      latency: item.latency > 0 ? parseFloat(item.latency.toFixed(2)) : null,
      isOnline: item.latency > 0,
      timestamp: item.timestamp,
    }));

    setChartData(recentData);

    // 트렌드 계산
    if (recentData.length >= 5) {
      const recent5 = recentData.slice(-5).filter((d) => d.latency !== null);
      const previous5 = recentData
        .slice(-10, -5)
        .filter((d) => d.latency !== null);

      if (recent5.length >= 3 && previous5.length >= 3) {
        const recentAvg =
          recent5.reduce((sum, d) => sum + d.latency, 0) / recent5.length;
        const previousAvg =
          previous5.reduce((sum, d) => sum + d.latency, 0) / previous5.length;
        const diff = ((recentAvg - previousAvg) / previousAvg) * 100;

        if (diff > 10) setTrend("up");
        else if (diff < -10) setTrend("down");
        else setTrend("stable");
      }
    }
  }, [data]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-900 dark:text-white">
            {label}
          </p>
          {data.isOnline ? (
            <p className="text-sm text-blue-600 dark:text-blue-400">
              레이턴시: {data.latency}ms
            </p>
          ) : (
            <p className="text-sm text-red-600 dark:text-red-400">오프라인</p>
          )}
        </div>
      );
    }
    return null;
  };

  const TrendIcon = () => {
    const iconProps = { className: "w-4 h-4" };
    switch (trend) {
      case "up":
        return <TrendingUp {...iconProps} className="w-4 h-4 text-red-500" />;
      case "down":
        return (
          <TrendingDown {...iconProps} className="w-4 h-4 text-green-500" />
        );
      default:
        return <Minus {...iconProps} className="w-4 h-4 text-gray-500" />;
    }
  };

  if (compact) {
    return (
      <div className="h-24">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient
                id={`colorLatency-${region}-${serverAddr}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="latency"
              stroke="#3b82f6"
              strokeWidth={2}
              fill={`url(#colorLatency-${region}-${serverAddr})`}
              connectNulls={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {title || `${region} - ${serverAddr}`}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            실시간 레이턴시 추이
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <TrendIcon />
          <span className="text-xs text-gray-500 dark:text-gray-400 capitalize">
            {trend === "up" ? "증가" : trend === "down" ? "감소" : "안정"}
          </span>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#e5e7eb"
              className="dark:stroke-gray-700"
            />
            <XAxis
              dataKey="time"
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              domain={["dataMin - 10", "dataMax + 10"]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="latency"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: "#3b82f6", strokeWidth: 2, r: 3 }}
              activeDot={{ r: 5, stroke: "#3b82f6", strokeWidth: 2 }}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 text-xs text-gray-500 dark:text-gray-400 text-center">
        최근 20개 측정값 표시 • 자동 업데이트
      </div>
    </div>
  );
};

export default LatencyChart;
