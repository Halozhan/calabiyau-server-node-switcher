using CommunityToolkit.Mvvm.ComponentModel;

namespace CalabiyauServerNodeSwitcher.Models
{
    public class Ping : ObservableObject
    {
        private const int SECONDS_TO_BE_SAVED = 10; // 10 seconds
        private const int PING_PER_SECOND = 100; // 100 pings per second
        private const int MAX_PING_COUNT = PING_PER_SECOND * SECONDS_TO_BE_SAVED;
        private readonly List<float> pingList;
        private readonly object lockObject = new object();

        public Ping()
        {
            pingList = new List<float>(MAX_PING_COUNT);
            recentAveragePing = 0.0;
            recentLossRate = 0.0;
            lowestPing = 0.0;
            highestPing = 0.0;
        }

        public float AddPing
        {
            set
            {
                lock (lockObject)
                {
                    while (pingList.Count >= MAX_PING_COUNT)
                    {
                        pingList.RemoveAt(0);
                    }
                    pingList.Add(value);

                    CalculateLastPing();
                    CalculateAveragePing();
                    CalculateRecentAveragePing();
                    CalculateLossRate();
                    CalculateRecentLossRate();
                    CalculateLowestPing();
                    CalculateHighestPing();
                    CalculateStdDeviation();
                    CalculateScore();
                }
            }
        }

        public void ClearPing()
        {
            lock (lockObject)
            {
                pingList.Clear();
                CalculateLastPing();
                CalculateAveragePing();
                CalculateRecentAveragePing();
                CalculateLossRate();
                CalculateRecentLossRate();
                CalculateLowestPing();
                CalculateHighestPing();
                CalculateStdDeviation();
                CalculateScore();
            }
        }

        // Last Ping
        private double lastPing;
        public double LastPing
        {
            get => lastPing;
            set => SetProperty(ref lastPing, value);
        }
        private void CalculateLastPing()
        {
            if (pingList.Count > 0)
            {
                LastPing = pingList.Last();
            }
            else
            {
                LastPing = 0;
            }
        }

        // 평균 Ping
        private double averagePing;
        public double AveragePing
        {
            get => averagePing;
            private set => SetProperty(ref averagePing, value);
        }
        private void CalculateAveragePing()
        {
            double sum = 0;
            int count = 0;

            foreach (var latency in pingList)
            {
                if (latency >= 0)
                {
                    sum += latency;
                    count++;
                }
            }
            AveragePing = sum / count;
        }

        // 최근 평균 Ping
        private double recentAveragePing;
        public double RecentAveragePing
        {
            get => recentAveragePing;
            private set => SetProperty(ref recentAveragePing, value);
        }
        private void CalculateRecentAveragePing()
        {
            double sum = 0;
            int count = 0;

            // 최근 1초 핑의 항목을 가져옵니다.
            var recentPingList = pingList.Skip(Math.Max(0, pingList.Count - PING_PER_SECOND)).Take(PING_PER_SECOND);

            foreach (var latency in recentPingList)
            {
                if (latency >= 0)
                {
                    sum += latency;
                    count++;
                }
            }
            RecentAveragePing = sum / count;
        }

        // 손실률
        private double lossRate;
        public double LossRate
        {
            get => lossRate;
            private set => SetProperty(ref lossRate, value);
        }
        private void CalculateLossRate()
        {
            int successCount = 0;
            int lossCount = 0;

            foreach (var latency in pingList)
            {
                if (latency >= 0)
                {
                    successCount++;
                }
                else
                {
                    lossCount++;
                }
            }
            LossRate = (double)lossCount / (successCount + lossCount) * 100;
        }

        // 최근 손실률
        private double recentLossRate;
        public double RecentLossRate
        {
            get => recentLossRate;
            private set => SetProperty(ref recentLossRate, value);
        }

        private void CalculateRecentLossRate()
        {
            int successCount = 0;
            int lossCount = 0;

            // 최근 1초 핑의 항목을 가져옵니다.
            var recentPingList = pingList.Skip(Math.Max(0, pingList.Count - PING_PER_SECOND)).Take(PING_PER_SECOND);

            foreach (var latency in recentPingList)
            {
                if (latency >= 0)
                {
                    successCount++;
                }
                else
                {
                    lossCount++;
                }
            }
            RecentLossRate = (double)lossCount / (successCount + lossCount) * 100;
        }

        // 최저 Ping
        private double lowestPing;
        public double LowestPing
        {
            get => lowestPing;
            private set => SetProperty(ref lowestPing, value);
        }
        private void CalculateLowestPing()
        {
            double min = double.MaxValue;

            foreach (var latency in pingList)
            {
                if (latency > 0 && latency < min)
                {
                    min = latency;
                }
            }
            LowestPing = min;
        }

        // 최고 Ping
        private double highestPing;
        public double HighestPing
        {
            get => highestPing;
            private set => SetProperty(ref highestPing, value);
        }
        private void CalculateHighestPing()
        {
            double max = double.MinValue;

            foreach (var latency in pingList)
            {
                if (latency > max)
                {
                    max = latency;
                }
            }
            HighestPing = max;
        }

        // 표준편차
        private double stdDeviation;
        public double StdDeviation
        {
            get => stdDeviation;
            private set => SetProperty(ref stdDeviation, value);
        }
        private void CalculateStdDeviation()
        {
            double sum = 0;
            int count = 0;

            foreach (var latency in pingList)
            {
                if (latency >= 0)
                {
                    sum += latency;
                    count++;
                }
            }
            double mean = sum / count;

            double sumOfSquaresOfDifferences = 0;

            foreach (var latency in pingList)
            {
                if (latency >= 0)
                {
                    sumOfSquaresOfDifferences += (latency - mean) * (latency - mean);
                }
            }
            StdDeviation = Math.Sqrt(sumOfSquaresOfDifferences / count);
        }

        // Score (lower is better)
        private double score;
        public double Score
        {
            get => score;
            private set => SetProperty(ref score, value);
        }
        private void CalculateScore()
        {
            Score = (AveragePing + StdDeviation) * (1 + LossRate / 4);
        }
    }
}
