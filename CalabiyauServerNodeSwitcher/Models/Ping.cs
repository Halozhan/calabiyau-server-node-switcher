using CommunityToolkit.Mvvm.ComponentModel;

namespace CalabiyauServerNodeSwitcher.Models
{
    public class Ping : ObservableObject
    {
        private const int MAX_PING_COUNT = 100 * 2;

        private readonly Queue<float> pingQueue;
        //private List<float> ping;
        public Ping()
        {
            //ping = new List<float>();
            pingQueue = new Queue<float>(MAX_PING_COUNT);
            averagePing = 0.0;
            lossRate = 0.0;
            lowestPing = double.MaxValue;
            highestPing = double.MinValue;
        }

        public float AddPing
        {
            set
            {
                //while (ping.Count >= MAX_PING_COUNT)
                //{
                //    ping.RemoveAt(0);
                //}
                //ping.Add(value);
                while (pingQueue.Count >= MAX_PING_COUNT)
                {
                    pingQueue.Dequeue();
                }
                pingQueue.Enqueue(value);
                CalculateAveragePing();
                CalculateLossRate();
                CalculateLowestPing();
                CalculateHighestPing();
                CalculateStdDeviation();
            }
        }

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
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
            {
                if (latency >= 0)
                {
                    sum += latency;
                    count++;
                }
            }
            AveragePing = sum / count;
        }

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
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
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

        private double lowestPing;
        public double LowestPing
        {
            get => lowestPing;
            private set => SetProperty(ref lowestPing, value);
        }

        private void CalculateLowestPing()
        {
            double min = double.MaxValue;
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
            {
                if (latency > 0 && latency < min)
                {
                    min = latency;
                }
            }
            LowestPing = min;
        }

        private double highestPing;
        public double HighestPing
        {
            get => highestPing;
            private set => SetProperty(ref highestPing, value);
        }

        private void CalculateHighestPing()
        {
            double max = double.MinValue;
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
            {
                if (latency > max)
                {
                    max = latency;
                }
            }
            HighestPing = max;
        }

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
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
            {
                if (latency >= 0)
                {
                    sum += latency;
                    count++;
                }
            }
            double mean = sum / count;

            double sumOfSquaresOfDifferences = 0;
            //foreach (var p in ping)
            foreach (var latency in pingQueue)
            {
                if (latency >= 0)
                {
                    sumOfSquaresOfDifferences += (latency - mean) * (latency - mean);
                }
            }
            StdDeviation = Math.Sqrt(sumOfSquaresOfDifferences / count);
        }
    }
}
