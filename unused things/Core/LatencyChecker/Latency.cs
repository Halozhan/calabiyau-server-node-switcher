using System.Collections.Concurrent;

namespace Core.LatencyChecker
{
    public class Latency
    {
        private const int MaxCapacity = 200;
        private readonly ConcurrentQueue<float> _latencies;

        public Latency()
        {
            _latencies = [];
        }

        public void Add(float ping)
        {
            _latencies.Enqueue(ping);
            while (_latencies.Count > MaxCapacity)
            {
                // 맨 앞의 요소 제거
                _latencies.TryDequeue(out _);
            }
        }

        public void Clear()
        {
            while (_latencies.TryDequeue(out _)) { }
        }

        public ConcurrentQueue<float> GetLatencyList()
        {
            return _latencies;
        }
    }
}
