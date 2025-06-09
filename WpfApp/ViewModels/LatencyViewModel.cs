using CommunityToolkit.Mvvm.ComponentModel;
using Core.LatencyChecker;
using System.Collections.Concurrent;

namespace WpfApp.ViewModels
{
    public partial class LatencyViewModel : ObservableObject
    {
        private Latency _latency;
        private LatencyService _latencyService;

        public LatencyViewModel(Latency latency)
        {
            _latency = latency;
            _latencyService = new LatencyService(latency);
        }

        public void Add(float ping)
        {
            _latency.Add(ping);
            _latencyService.Update();
            OnPropertyChanged(nameof(Average));
            OnPropertyChanged(nameof(Min));
            OnPropertyChanged(nameof(Max));
            OnPropertyChanged(nameof(LossRate));
            OnPropertyChanged(nameof(StandardDeviation));
            OnPropertyChanged(nameof(Score));
        }

        public async Task AddAsync(float ping)
        {
            await Task.Run(() => Add(ping));
        }

        public void Clear()
        {
            _latency.Clear();
        }

        public ConcurrentQueue<float> GetLatencyList()
        {
            return _latency.GetLatencyList();
        }

        public float Average => _latencyService.Average;
        public float Min => _latencyService.Min;
        public float Max => _latencyService.Max;
        public float LossRate => _latencyService.LossRate;
        public float StandardDeviation => _latencyService.StandardDeviation;
        public float Score => _latencyService.Score;
    }
}
