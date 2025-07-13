import { useState, useEffect, useCallback } from "react";

// 서버 목록을 가져오는 훅
export const useServers = (refreshInterval = 10000) => {
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchServers = useCallback(async () => {
    try {
      const response = await fetch("/api/servers");
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setServers(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error("Failed to fetch servers:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchServers();
    const interval = setInterval(fetchServers, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchServers, refreshInterval]);

  return { servers, loading, error, refetch: fetchServers };
};

// 특정 서버의 통계를 가져오는 훅
export const useServerStats = (
  region,
  serverAddr,
  window = 30,
  refreshInterval = 1000
) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = useCallback(async () => {
    if (!region || !serverAddr) return;

    try {
      const params = new URLSearchParams({
        region,
        server_addr: serverAddr,
        window: window.toString(),
      });

      const response = await fetch(`/api/stats?${params}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error("Failed to fetch stats:", err);
    } finally {
      setLoading(false);
    }
  }, [region, serverAddr, window]);

  useEffect(() => {
    if (region && serverAddr) {
      fetchStats();
      const interval = setInterval(fetchStats, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchStats, refreshInterval, region, serverAddr]);

  return { stats, loading, error, refetch: fetchStats };
};

// 설정을 가져오고 업데이트하는 훅
export const useConfig = () => {
  const [config, setConfig] = useState({ interval_ms: 100 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchConfig = useCallback(async () => {
    try {
      const response = await fetch("/api/config");
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setConfig(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error("Failed to fetch config:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateConfig = useCallback(async (newInterval) => {
    try {
      const response = await fetch(`/api/config?interval_ms=${newInterval}`, {
        method: "POST",
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setConfig(data);
      setError(null);
      return true;
    } catch (err) {
      setError(err.message);
      console.error("Failed to update config:", err);
      return false;
    }
  }, []);

  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  return { config, loading, error, updateConfig, refetch: fetchConfig };
};

// WebSocket 연결을 위한 훅 (향후 확장용)
export const useWebSocket = (url, options = {}) => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setConnected(true);
      setSocket(ws);
    };

    ws.onmessage = (event) => {
      setLastMessage(JSON.parse(event.data));
    };

    ws.onclose = () => {
      setConnected(false);
      setSocket(null);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = useCallback(
    (message) => {
      if (socket && connected) {
        socket.send(JSON.stringify(message));
      }
    },
    [socket, connected]
  );

  return { connected, lastMessage, sendMessage };
};
