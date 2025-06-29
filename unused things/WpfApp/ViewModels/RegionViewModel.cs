using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Core.HostsManager;
using System.Timers;

namespace WpfApp.ViewModels
{
    public partial class RegionViewModel : ObservableObject, IRegionViewModel
    {
        private System.Timers.Timer _timer;

        [ObservableProperty]
        private NodeViewModel _worstServer;

        //[ObservableProperty]
        //private NodeViewModel _bestEdgeOne;

        public string Name { get; set; }
        public string RegionCode { get; }
        public INodeListViewModel Server { get; set; }
        //public INodeListViewModel EdgeOne { get; set; }

        public RegionViewModel(string name, string regionCode)
        {
            Name = name;
            RegionCode = regionCode;
            Server = new NodeListViewModel();
            //EdgeOne = new NodeListViewModel();
            IsApplyAccelerator = [];

            _timer = new System.Timers.Timer(1000); // 간격마다 업데이트
            _timer.Elapsed += OnTimerElapsed;
            _timer.Start();
        }

        private void OnTimerElapsed(object sender, ElapsedEventArgs e)
        {
            UpdateWorstServer();
            //UpdateBestEdgeOne();
            //UpdateBestServer();
        }

        private void UpdateWorstServer()
        {
            var list = Server.NodeList.ToList();
            var worstServer = list.MaxBy(node => node.Latency.Score);
            if (worstServer != _worstServer)
            {
                WorstServer = worstServer;
            }
        }

        private void UpdateBestEdgeOne()
        {
            //var list = EdgeOne.NodeList.ToList();
            //var bestEdgeOne = list.MinBy(node => node.Latency.Score);
            //if (bestEdgeOne != _bestEdgeOne)
            //{
            //    BestEdgeOne = bestEdgeOne;
            //}
        }

        public Dictionary<string, bool> IsApplyAccelerator { get; set; }

        private void UpdateBestServer()
        {
            //foreach (var node in Server.NodeList)
            //{
            //    var ipAddress = node.Address.ToString();
            //    var isAccelerated = node.Latency.Score > BestEdgeOne.Latency.Score;
            //    IsApplyAccelerator[ipAddress] = isAccelerated;
            //}
        }

        [RelayCommand]
        private void UpdateHosts()
        {
            var hostsManager = HostsManager.GetInstance();
            hostsManager.LoadHosts();

            var nodeList = Server.NodeList.ToList();
            foreach (var node in nodeList)
            {
                IsApplyAccelerator.TryGetValue(node.Address.ToString(), out bool isAccelerated);
                //string ipAddress = isAccelerated ? BestEdgeOne.Address.ToString() : node.Address.ToString();
                string ipAddress = node.Address.ToString();

                // EdgeOne
                //string hostname = $"klbqcp-prod-ds-{RegionCode}{node.Number}-eo.gxpan.cn";
                //Host host = new Host(ipAddress, hostname);
                //hostsManager.AddOrChangeHost(host);

                // Server
                string hostname = $"klbqcp-prod-ds-{RegionCode}{node.Number}-server.gxpan.cn";
                Host host = new Host(ipAddress, hostname);
                hostsManager.AddOrChangeHost(host);
            }

            hostsManager.UpdateHostsFile();
        }
    }
}
