import React from "react";
import {
  Server,
  Settings,
  Moon,
  Sun,
  Activity,
  Wifi,
  WifiOff,
} from "lucide-react";
import { toggleDarkMode } from "../utils/helpers";

const Header = ({
  totalServers,
  onlineServers,
  onSettingsClick,
  isDarkMode,
  setIsDarkMode,
}) => {
  const handleDarkModeToggle = () => {
    toggleDarkMode();
    setIsDarkMode(!isDarkMode);
  };

  const connectionRate =
    totalServers > 0 ? (onlineServers / totalServers) * 100 : 0;

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* 로고 및 타이틀 */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Activity className="w-8 h-8 text-primary-600 dark:text-primary-400" />
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  Calabiyau Monitor
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Server Node Switcher
                </p>
              </div>
            </div>
          </div>

          {/* 중앙 통계 */}
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <Server className="w-5 h-5 text-gray-400" />
              <span className="text-sm text-gray-600 dark:text-gray-300">
                서버: <span className="font-semibold">{totalServers}</span>
              </span>
            </div>

            <div className="flex items-center space-x-2">
              {onlineServers === totalServers ? (
                <Wifi className="w-5 h-5 text-green-500" />
              ) : (
                <WifiOff className="w-5 h-5 text-red-500" />
              )}
              <span className="text-sm text-gray-600 dark:text-gray-300">
                온라인:{" "}
                <span className="font-semibold text-green-600 dark:text-green-400">
                  {onlineServers}
                </span>
              </span>
            </div>

            {/* 연결률 표시 */}
            <div className="flex items-center space-x-2">
              <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-500 ${
                    connectionRate >= 80
                      ? "bg-green-500"
                      : connectionRate >= 60
                      ? "bg-yellow-500"
                      : "bg-red-500"
                  }`}
                  style={{ width: `${Math.max(connectionRate, 5)}%` }}
                />
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                {connectionRate.toFixed(1)}%
              </span>
            </div>
          </div>

          {/* 우측 액션 버튼들 */}
          <div className="flex items-center space-x-2">
            {/* 다크 모드 토글 */}
            <button
              onClick={handleDarkModeToggle}
              className="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="다크 모드 토글"
            >
              {isDarkMode ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </button>

            {/* 설정 버튼 */}
            <button
              onClick={onSettingsClick}
              className="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="설정"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 모바일용 통계 */}
        <div className="md:hidden pb-3 flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            <span className="text-gray-600 dark:text-gray-300">
              총 {totalServers}대 | 온라인 {onlineServers}대
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  connectionRate >= 80
                    ? "bg-green-500"
                    : connectionRate >= 60
                    ? "bg-yellow-500"
                    : "bg-red-500"
                }`}
                style={{ width: `${Math.max(connectionRate, 5)}%` }}
              />
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
              {connectionRate.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
