SELECT -- region,
    domain,
    server_addr,
    -- port,
    AVG(
        CASE
            WHEN latency > 0 THEN latency
        END
    ) AS avg_latency,
    MIN(
        CASE
            WHEN latency > 0 THEN latency
        END
    ) AS min_latency,
    MAX(
        CASE
            WHEN latency > 0 THEN latency
        END
    ) AS max_latency,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN latency = -1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS loss_rate_percent
FROM latency
WHERE timestamp >= (
        SELECT MAX(timestamp)
        FROM latency
    ) - 10
GROUP BY region,
    domain,
    server_addr,
    port;