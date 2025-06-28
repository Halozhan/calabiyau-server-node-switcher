import React, { useEffect, useState } from "react";

function LatencyStats({ region, serverAddr }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = () => {
      fetch(
        `/api/stats?region=${encodeURIComponent(
          region
        )}&server_addr=${encodeURIComponent(serverAddr)}&window=30`
      )
        .then((res) => res.json())
        .then(setStats);
    };
    fetchStats();
    const interval = setInterval(fetchStats, 1000);
    return () => clearInterval(interval);
  }, [region, serverAddr]);

  if (!stats) return <div>Loading...</div>;
  return (
    <div>
      <h3>
        {region} - {serverAddr}
      </h3>
      <ul>
        <li>평균: {stats.avg !== null ? stats.avg.toFixed(2) : "N/A"} ms</li>
        <li>최소: {stats.min !== null ? stats.min.toFixed(2) : "N/A"} ms</li>
        <li>최대: {stats.max !== null ? stats.max.toFixed(2) : "N/A"} ms</li>
        <li>
          손실률:{" "}
          {stats.loss_rate !== null
            ? (stats.loss_rate * 100).toFixed(1) + "%"
            : "N/A"}
        </li>
        <li>측정 개수: {stats.count}</li>
      </ul>
    </div>
  );
}

export default LatencyStats;
