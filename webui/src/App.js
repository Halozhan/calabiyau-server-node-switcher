import React, { useState, useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import ServerCard from "./components/ServerCard";
import LatencyChart from "./components/LatencyChart";
import { useServers, useServerStats } from "./hooks/useApi";
import { initDarkMode } from "./utils/helpers";
import {
  ChevronDown,
  ChevronUp,
  Search,
  BarChart3,
  Grid,
  List,
} from "lucide-react";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [selectedServer, setSelectedServer] = useState(null);
  const [viewMode, setViewMode] = useState("grid"); // 'grid', 'list', 'chart'
  const [searchTerm, setSearchTerm] = useState("");
  const [showCharts, setShowCharts] = useState(false);
  const [sortBy, setSortBy] = useState("region"); // 'region', 'latency', 'status'
  const [filterStatus, setFilterStatus] = useState("all"); // 'all', 'online', 'offline'

  // API 훅들
  const {
    servers,
    loading: serversLoading,
    error: serversError,
  } = useServers();
  const { stats: selectedStats } = useServerStats(
    selectedServer?.region,
    selectedServer?.server_addr,
    30,
    1000
  );

  // 다크 모드 초기화
  useEffect(() => {
    initDarkMode();
    setIsDarkMode(document.documentElement.classList.contains("dark"));
  }, []);

  // 서버 통계 상태 관리
  const [allStats, setAllStats] = useState({});

  // 모든 서버의 통계를 주기적으로 가져오기
  useEffect(() => {
    if (!servers.length) return;

    const fetchAllStats = async () => {
      const statsPromises = servers.map(async (server) => {
        try {
          const params = new URLSearchParams({
            region: server.region,
            server_addr: server.server_addr,
            window: "30",
          });
          const response = await fetch(`/api/stats?${params}`);
          if (response.ok) {
            const data = await response.json();
            return { key: `${server.region}-${server.server_addr}`, data };
          }
        } catch (error) {
          console.error(`Failed to fetch stats for ${server.region}:`, error);
        }
        return null;
      });

      const results = await Promise.all(statsPromises);
      const newStats = {};
      results.forEach((result) => {
        if (result) {
          newStats[result.key] = result.data;
        }
      });
      setAllStats(newStats);
    };

    fetchAllStats();
    const interval = setInterval(fetchAllStats, 2000);
    return () => clearInterval(interval);
  }, [servers]);

  // 필터링 및 정렬된 서버 목록
  const filteredAndSortedServers = React.useMemo(() => {
    let filtered = servers.filter((server) => {
      const matchesSearch =
        server.region.toLowerCase().includes(searchTerm.toLowerCase()) ||
        server.server_addr.toLowerCase().includes(searchTerm.toLowerCase());

      if (!matchesSearch) return false;

      const stats = allStats[`${server.region}-${server.server_addr}`];
      if (filterStatus === "online") {
        return stats && stats.avg > 0;
      } else if (filterStatus === "offline") {
        return !stats || stats.avg <= 0;
      }
      return true;
    });

    // 정렬
    filtered.sort((a, b) => {
      const statsA = allStats[`${a.region}-${a.server_addr}`];
      const statsB = allStats[`${b.region}-${b.server_addr}`];

      switch (sortBy) {
        case "latency":
          const latencyA = statsA?.avg || 9999;
          const latencyB = statsB?.avg || 9999;
          return latencyA - latencyB;
        case "status":
          const statusA = statsA?.avg > 0 ? 1 : 0;
          const statusB = statsB?.avg > 0 ? 1 : 0;
          return statusB - statusA;
        default: // region
          return a.region.localeCompare(b.region);
      }
    });

    return filtered;
  }, [servers, allStats, searchTerm, filterStatus, sortBy]);

  // 온라인 서버 수 계산
  const onlineServers = filteredAndSortedServers.filter((server) => {
    const stats = allStats[`${server.region}-${server.server_addr}`];
    return stats && stats.avg > 0;
  }).length;

  const handleServerClick = (server) => {
    setSelectedServer(server);
  };

  const handleSettingsClick = () => {
    // 설정 모달 표시 (향후 구현)
    alert("설정 기능은 향후 구현 예정입니다.");
  };

  if (serversLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">
            서버 목록을 불러오는 중...
          </p>
        </div>
      </div>
    );
  }

  if (serversError) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 dark:text-red-400 mb-4">
            서버 연결 오류: {serversError}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <Header
        totalServers={servers.length}
        onlineServers={onlineServers}
        onSettingsClick={handleSettingsClick}
        isDarkMode={isDarkMode}
        setIsDarkMode={setIsDarkMode}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 필터 및 검색 컨트롤 */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            {/* 검색 */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="서버 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* 컨트롤 버튼들 */}
            <div className="flex items-center space-x-2">
              {/* 뷰 모드 */}
              <div className="flex items-center space-x-1 bg-white dark:bg-gray-800 rounded-lg border border-gray-300 dark:border-gray-600 p-1">
                <button
                  onClick={() => setViewMode("grid")}
                  className={`p-2 rounded ${
                    viewMode === "grid"
                      ? "bg-primary-600 text-white"
                      : "text-gray-600 dark:text-gray-400"
                  }`}
                  title="그리드 보기"
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode("list")}
                  className={`p-2 rounded ${
                    viewMode === "list"
                      ? "bg-primary-600 text-white"
                      : "text-gray-600 dark:text-gray-400"
                  }`}
                  title="리스트 보기"
                >
                  <List className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode("chart")}
                  className={`p-2 rounded ${
                    viewMode === "chart"
                      ? "bg-primary-600 text-white"
                      : "text-gray-600 dark:text-gray-400"
                  }`}
                  title="차트 보기"
                >
                  <BarChart3 className="w-4 h-4" />
                </button>
              </div>

              {/* 정렬 */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
              >
                <option value="region">지역순</option>
                <option value="latency">레이턴시순</option>
                <option value="status">상태순</option>
              </select>

              {/* 필터 */}
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">전체</option>
                <option value="online">온라인만</option>
                <option value="offline">오프라인만</option>
              </select>

              {/* 차트 토글 */}
              <button
                onClick={() => setShowCharts(!showCharts)}
                className={`px-3 py-2 rounded-lg border transition-colors ${
                  showCharts
                    ? "bg-primary-600 text-white border-primary-600"
                    : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700"
                }`}
                title="차트 표시 토글"
              >
                {showCharts ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* 서버 그리드/리스트 */}
        {viewMode === "chart" && selectedServer ? (
          <div className="mb-8">
            <LatencyChart
              data={selectedStats?.raw_data}
              title={`${selectedServer.region} - ${selectedServer.server_addr}`}
              region={selectedServer.region}
              serverAddr={selectedServer.server_addr}
            />
          </div>
        ) : null}

        <div
          className={`grid gap-6 ${
            viewMode === "list"
              ? "grid-cols-1"
              : "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
          }`}
        >
          {filteredAndSortedServers.map((server) => {
            const stats = allStats[`${server.region}-${server.server_addr}`];
            return (
              <ServerCard
                key={`${server.region}-${server.server_addr}`}
                region={server.region}
                serverAddr={server.server_addr}
                stats={stats}
                isSelected={
                  selectedServer?.region === server.region &&
                  selectedServer?.server_addr === server.server_addr
                }
                onClick={() => handleServerClick(server)}
                showChart={showCharts}
              />
            );
          })}
        </div>

        {filteredAndSortedServers.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">
              검색 조건에 맞는 서버가 없습니다.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
