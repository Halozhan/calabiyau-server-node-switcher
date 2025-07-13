import React from "react";
import {
  Server,
  Wifi,
  WifiOff,
  Clock,
  TrendingUp,
  TrendingDown,
  Activity,
  AlertTriangle,
} from "lucide-react";
import {
  getLatencyStatus,
  getStatusColor,
  getStatusDotColor,
  formatNumber,
  formatPercent,
} from "../utils/helpers";
import LatencyChart from "./LatencyChart";

const ServerCard = ({
  region,
  serverAddr,
  stats,
  isSelected,
  onClick,
  showChart = false,
}) => {
  if (!stats) {
    return (
      <div className="metric-card opacity-50">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="status-indicator bg-gray-400" />
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {region}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {serverAddr}
              </p>
            </div>
          </div>
          <WifiOff className="w-5 h-5 text-gray-400" />
        </div>
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">데이터 로딩 중...</p>
        </div>
      </div>
    );
  }

  const status = getLatencyStatus(stats.avg || -1);
  const statusColor = getStatusColor(status);
  const dotColor = getStatusDotColor(status);

  const getStatusIcon = () => {
    switch (status) {
      case "offline":
        return <WifiOff className="w-5 h-5 text-red-500" />;
      case "excellent":
        return <Wifi className="w-5 h-5 text-green-500" />;
      case "good":
        return <Wifi className="w-5 h-5 text-blue-500" />;
      case "fair":
        return <Activity className="w-5 h-5 text-yellow-500" />;
      case "poor":
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
      default:
        return <WifiOff className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "offline":
        return "오프라인";
      case "excellent":
        return "매우 좋음";
      case "good":
        return "좋음";
      case "fair":
        return "보통";
      case "poor":
        return "나쁨";
      default:
        return "알 수 없음";
    }
  };

  return (
    <div
      className={`metric-card cursor-pointer transition-all duration-200 ${
        isSelected ? "ring-2 ring-primary-500 shadow-lg" : "hover:shadow-md"
      }`}
      onClick={onClick}
    >
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`status-indicator ${dotColor}`} />
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              {region}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {serverAddr}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <span
            className={`text-xs px-2 py-1 rounded-full border ${statusColor}`}
          >
            {getStatusText()}
          </span>
        </div>
      </div>

      {/* 메트릭 그리드 */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-blue-500" />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              평균
            </span>
          </div>
          <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
            {formatNumber(stats.avg)} ms
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div className="flex items-center space-x-2">
            <TrendingDown className="w-4 h-4 text-green-500" />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              최소
            </span>
          </div>
          <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
            {formatNumber(stats.min)} ms
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-red-500" />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              최대
            </span>
          </div>
          <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
            {formatNumber(stats.max)} ms
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-orange-500" />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              손실률
            </span>
          </div>
          <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
            {formatPercent(stats.loss_rate)}
          </p>
        </div>
      </div>

      {/* 작은 차트 (옵션) */}
      {showChart && stats.raw_data && (
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
          <LatencyChart
            data={stats.raw_data}
            region={region}
            serverAddr={serverAddr}
            compact={true}
          />
        </div>
      )}

      {/* 푸터 */}
      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2">
          <Server className="w-3 h-3" />
          <span>측정 수: {stats.count}</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span>실시간</span>
        </div>
      </div>
    </div>
  );
};

export default ServerCard;
