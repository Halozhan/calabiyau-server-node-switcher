import React, { useEffect, useState } from "react";
import LatencyStats from "./LatencyStats";

function AllServersStats() {
  const [serverList, setServerList] = useState([]);

  useEffect(() => {
    const fetchServers = () => {
      fetch("/api/servers")
        .then((res) => res.json())
        .then(setServerList);
    };
    fetchServers();
    const interval = setInterval(fetchServers, 10000); // 10초마다 서버 목록 갱신
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>모든 서버 실시간 통계</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
        {serverList.length === 0 && <div>서버 목록을 불러오는 중...</div>}
        {serverList.map(({ region, server_addr }) => (
          <div
            key={region + server_addr}
            style={{
              border: "1px solid #ccc",
              borderRadius: 8,
              padding: 12,
              minWidth: 260,
            }}
          >
            <LatencyStats region={region} serverAddr={server_addr} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default AllServersStats;
