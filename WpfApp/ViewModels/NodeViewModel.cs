using CommunityToolkit.Mvvm.ComponentModel;
using Core.LatencyChecker;
using Core.Node;

namespace WpfApp.ViewModels
{
    public partial class NodeViewModel : ObservableObject
    {
        private Node _node;

        [ObservableProperty]
        public int _number;

        public string IPAddress => _node.IPAddress.ToString();
        public int Port => _node.Port;

        public LatencyViewModel Latency { get; set; }

        [ObservableProperty]
        private LatencyService _latencyService;

        private readonly UDPSession _udpSession;

        public NodeViewModel(Node node, int number = 0)
        {
            _node = node;
            _number = number;

            Latency latency = new();
            Latency = new LatencyViewModel(latency);
            LatencyService = new LatencyService(latency);

            _udpSession = new UDPSession(_node.IPAddress, _node.Port, Latency.AddAsync);
            StartSession();
            //Task.Run(async () =>
            //{
            //    while (true)
            //    {
            //        await TestSession();
            //    }
            //});
        }

        public async Task TestSession()
        {
            Random random = new();

            await Task.Run(async () =>
            {
                Latency.Add(random.Next(-1, 100));
                await Task.Delay(100);
            });
        }

        public void StartSession()
        {
            _udpSession.Start();
        }

        public void StopSession()
        {
            _udpSession.Stop();
        }

        public string Address => _node.IPAddress.ToString();
    }
}
