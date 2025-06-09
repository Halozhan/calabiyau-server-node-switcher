namespace Core.LatencyChecker
{
    public class LatencyService(Latency latency)
    {
        private List<float> _latencyList = [];
        private readonly Latency _latency = latency;

        public void Update()
        {
            _latencyList = _latency.GetLatencyList().ToList();
            RemovedOutlier = CalculateOutlier();
            Average = CalculateAverage();
            Min = CalculateMin();
            Max = CalculateMax();
            LossRate = CalculateLossRate();
            StandardDeviation = CalculateStandardDeviation();
            Score = CalculateScore();
        }

        // 이상치 제거
        public List<float> RemovedOutlier = [];
        private List<float> CalculateOutlier()
        {
            if (_latencyList.Count == 0) return [];
            // 0 미만이거나 1000 초과인 값 제거
            return _latency.GetLatencyList().Where(ping => ping >= 0 && ping <= 1000).ToList();
        }

        public float Average = 0;
        private float CalculateAverage()
        {
            if (RemovedOutlier.Count == 0) return -1;
            return RemovedOutlier.Average();
        }

        public float Min = 0;
        private float CalculateMin()
        {
            if (RemovedOutlier.Count == 0) return -1;
            return RemovedOutlier.Min();
        }

        public float Max = 0;
        private float CalculateMax()
        {
            if (RemovedOutlier.Count == 0) return -1;
            return RemovedOutlier.Max();
        }

        public float LossRate = 0;
        private float CalculateLossRate()
        {
            if (_latencyList.Count == 0) return -1;
            return (float)_latencyList.Count(ping => ping == -1) / _latencyList.Count;
        }

        public float StandardDeviation = 0;
        private float CalculateStandardDeviation()
        {
            if (RemovedOutlier.Count == 0) return -1;
            return (float)Math.Sqrt(RemovedOutlier.Average(ping => Math.Pow(ping - Average, 2)));
        }

        public float Score = 0;
        private float CalculateScore()
        {
            if (_latency.GetLatencyList().Count == 0) return -1;
            // https://www.desmos.com/calculator/a5ytt48rmk
            return (float)((Average + StandardDeviation) * Math.Pow(100, LossRate));
        }
    }
}
