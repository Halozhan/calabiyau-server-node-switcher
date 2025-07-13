// 레이턴시 값에 따른 상태 분류
export const getLatencyStatus = (latency) => {
  if (latency < 0) return "offline";
  if (latency < 50) return "excellent";
  if (latency < 100) return "good";
  if (latency < 200) return "fair";
  return "poor";
};

// 상태에 따른 색상 반환
export const getStatusColor = (status) => {
  const colors = {
    offline: "text-red-500 bg-red-50 border-red-200",
    excellent: "text-green-500 bg-green-50 border-green-200",
    good: "text-blue-500 bg-blue-50 border-blue-200",
    fair: "text-yellow-500 bg-yellow-50 border-yellow-200",
    poor: "text-red-500 bg-red-50 border-red-200",
  };
  return colors[status] || colors.offline;
};

// 상태에 따른 점 색상 반환
export const getStatusDotColor = (status) => {
  const colors = {
    offline: "bg-red-500",
    excellent: "bg-green-500",
    good: "bg-blue-500",
    fair: "bg-yellow-500",
    poor: "bg-red-500",
  };
  return colors[status] || colors.offline;
};

// 숫자 포맷팅 (소수점 자릿수 제한)
export const formatNumber = (num, decimals = 2) => {
  if (num === null || num === undefined) return "N/A";
  if (num < 0) return "Offline";
  return Number(num).toFixed(decimals);
};

// 퍼센트 포맷팅
export const formatPercent = (num, decimals = 1) => {
  if (num === null || num === undefined) return "N/A";
  return `${(num * 100).toFixed(decimals)}%`;
};

// 시간 포맷팅
export const formatTime = (timestamp) => {
  return new Date(timestamp * 1000).toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

// 레이턴시 차트 데이터 준비
export const prepareChartData = (data, maxPoints = 20) => {
  if (!data || !Array.isArray(data)) return [];

  return data.slice(-maxPoints).map((item, index) => ({
    time: formatTime(item.timestamp),
    latency: item.latency > 0 ? item.latency : null,
    isOnline: item.latency > 0,
  }));
};

// 다크 모드 토글
export const toggleDarkMode = () => {
  const root = document.documentElement;
  root.classList.toggle("dark");
  localStorage.setItem("darkMode", root.classList.contains("dark"));
};

// 다크 모드 초기화
export const initDarkMode = () => {
  const savedMode = localStorage.getItem("darkMode");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedMode === "true" || (savedMode === null && prefersDark)) {
    document.documentElement.classList.add("dark");
  }
};
