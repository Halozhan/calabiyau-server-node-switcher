using CalabiyauServerNodeSwitcher.Models;
using CalabiyauServerNodeSwitcher.Services;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Diagnostics;
using System.Windows.Input;

namespace CalabiyauServerNodeSwitcher.ViewModels
{
    public class ServerListViewModel : ObservableObject
    {
        private CancellationTokenSource _cancellationTokenSource;

        public ServerListViewModel()
        {
            InitServerList();
            ToggleAutoFindCommand = new RelayCommand(ToggleAutoFind);
            RefreshCommand = new RelayCommand(Refresh);
            ResetCommand = new RelayCommand(Reset);
            GroupButtonCommand = new RelayCommand(ExecuteGroupButtonCommand);
            Task.Run(() => UpdatePingEach());
        }

        private List<ServerInfo> _chongqingServerList = new List<ServerInfo>();
        public List<ServerInfo> ChongqingServerList
        {
            get => _chongqingServerList;
            set => SetProperty(ref _chongqingServerList, value);
        }

        private List<ServerInfo> _tianjinServerList = new List<ServerInfo>();
        public List<ServerInfo> TianjinServerList
        {
            get => _tianjinServerList;
            set => SetProperty(ref _tianjinServerList, value);
        }

        private List<ServerInfo> _nanjingServerList = new List<ServerInfo>();
        public List<ServerInfo> NanjingServerList
        {
            get => _nanjingServerList;
            set => SetProperty(ref _nanjingServerList, value);
        }

        private List<ServerInfo> _guangzhouServerList = new List<ServerInfo>();
        public List<ServerInfo> GuangzhouServerList
        {
            get => _guangzhouServerList;
            set => SetProperty(ref _guangzhouServerList, value);
        }

        private void InitServerList()
        {
            // chongqing
            ChongqingServerList = new List<ServerInfo>
            {
                //new ServerInfo { IPAddress = "111.10.11.250", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "111.10.11.73", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "113.250.9.54", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "113.250.9.56", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "175.27.48.249", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "175.27.49.194", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.159.233.98", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "58.144.164.43", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "58.144.164.50", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "119.45.28.76", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.134.150.4", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.253.232", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.252.232", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "129.226.82.90", Ping = new Ping(), IsSelected = false, Domain = "ds-cq-1.klbq.qq.com" },
            };

            string chongqingIP = HostsManager.Instance.GetIPAddress("ds-cq-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in ChongqingServerList)
            {
                if (serverInfo.IPAddress == chongqingIP)
                {
                    serverInfo.IsSelected = true;
                }
            }

            // tianjin
            TianjinServerList = new List<ServerInfo>
            {
                //new ServerInfo { IPAddress = "109.244.173.239", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "109.244.173.251", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "111.30.170.175", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "111.33.110.226", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "116.130.228.105", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "116.130.229.177", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "123.151.54.47", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "42.81.194.60", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.159.233.14", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" }
                new ServerInfo { IPAddress = "43.132.138.189", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.252.41", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.253.41", Ping = new Ping(), IsSelected = false, Domain = "ds-tj-1.klbq.qq.com" },
            };

            string tianjinIP = HostsManager.Instance.GetIPAddress("ds-tj-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in TianjinServerList)
            {
                if (serverInfo.IPAddress == tianjinIP)
                {
                    serverInfo.IsSelected = true;
                }
            }

            // guangzhou
            GuangzhouServerList = new List<ServerInfo>
            {
                //new ServerInfo { IPAddress = "120.232.24.96", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "120.233.18.175", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "14.29.103.46", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "157.148.58.53", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "157.255.4.48", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "183.47.107.193", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.139.252.183", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.141.58.200", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.159.233.178", Ping = new Ping(), IsSelected = false, Domain = "ds-gz-1.klbq.qq.com" }
                new ServerInfo { IPAddress = "43.175.253.233", Domain = "ds-gz-1.klbq.qq.com", Ping = new Ping(), IsSelected = false },
            };

            string guangzhouIP = HostsManager.Instance.GetIPAddress("ds-gz-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in GuangzhouServerList)
            {
                if (serverInfo.IPAddress == guangzhouIP)
                {
                    serverInfo.IsSelected = true;
                }
            }

            // nanjing
            NanjingServerList = new List<ServerInfo>
            {
                //new ServerInfo { IPAddress = "112.80.183.27", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "121.229.92.16", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "180.110.193.185", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "182.50.15.118", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "36.155.164.82", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "36.155.183.208", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.141.129.109", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.141.129.21", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                //new ServerInfo { IPAddress = "43.159.233.198", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.163.252.167", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.227.191", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
                new ServerInfo { IPAddress = "43.175.226.191", Ping = new Ping(), IsSelected = false, Domain = "ds-nj-1.klbq.qq.com" },
            };
            string nanjingIP = HostsManager.Instance.GetIPAddress("ds-nj-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in NanjingServerList)
            {
                if (serverInfo.IPAddress == nanjingIP)
                {
                    serverInfo.IsSelected = true;
                }
            }
        }

        private bool isAutoFindEnabled;
        public bool IsAutoFindEnabled
        {
            get => isAutoFindEnabled;
            set => SetProperty(ref isAutoFindEnabled, value);
        }

        public ICommand ToggleAutoFindCommand { get; }
        public ICommand RefreshCommand { get; }
        public ICommand ResetCommand { get; }

        private void ToggleAutoFind()
        {
            // Implement the logic to enable/disable auto-find
            if (IsAutoFindEnabled)
            {
                _cancellationTokenSource = new CancellationTokenSource();
                Task.Run(() => SelectBestServer(_cancellationTokenSource.Token));
            }
            else
            {
                _cancellationTokenSource.Cancel();
            }
        }

        private void Refresh()
        {
            // Implement the logic to refresh the server list
            ChongqingServerList.ForEach(s => s.Ping.ClearPing());
            TianjinServerList.ForEach(s => s.Ping.ClearPing());
            GuangzhouServerList.ForEach(s => s.Ping.ClearPing());
            NanjingServerList.ForEach(s => s.Ping.ClearPing());
        }

        private void Reset()
        {
            // Set IsAutoFindEnabled to false and notify the UI
            IsAutoFindEnabled = false;

            // Cancel the ongoing task if any
            _cancellationTokenSource?.Cancel();

            // Remove domains from HostsManager
            HostsManager.Instance.RemoveDomain("ds-cq-1.klbq.qq.com");
            HostsManager.Instance.RemoveDomain("ds-tj-1.klbq.qq.com");
            HostsManager.Instance.RemoveDomain("ds-gz-1.klbq.qq.com");
            HostsManager.Instance.RemoveDomain("ds-nj-1.klbq.qq.com");

            // Deselect all servers
            ChongqingServerList.ForEach(s => s.IsSelected = false);
            TianjinServerList.ForEach(s => s.IsSelected = false);
            GuangzhouServerList.ForEach(s => s.IsSelected = false);
            NanjingServerList.ForEach(s => s.IsSelected = false);
        }

        private void UpdatePingEach()
        {
            var allServers = new List<ServerInfo>();
            allServers.AddRange(ChongqingServerList);
            allServers.AddRange(TianjinServerList);
            allServers.AddRange(GuangzhouServerList);
            allServers.AddRange(NanjingServerList);

            foreach (ServerInfo serverInfo in allServers)
            {
                Task.Run(() => UpdatePing(serverInfo));
            }
        }

        private static async void UpdatePing(ServerInfo serverInfo)
        {
            const ushort SECOND = 1000;
            const ushort PACKET_PER_SECOND = 10;
            const ushort PING_INTERVAL = SECOND / PACKET_PER_SECOND;
            const uint REFRESH_CONNECTION_SECOND = 5;
            const uint REFRESH_INTERVAL = PACKET_PER_SECOND * REFRESH_CONNECTION_SECOND;
            const ushort PORT = 20000;
            var udpClient = new GetUDPPingTime(serverInfo.IPAddress, PORT);

            while (true)
            {
                var pingTasks = new List<Task>();

                for (int i = 0; i < REFRESH_INTERVAL; i++)
                {
                    pingTasks.Add(Task.Run(() => serverInfo.Ping.AddPing = udpClient.QueryPing()));
                    await Task.Delay(PING_INTERVAL);
                }

                await Task.WhenAll(pingTasks);
                udpClient.ClientClose();
            }
        }

        private void SelectBestServer(CancellationToken cancellationToken)
        {
            const int UPDATE_INTERVAL = 1000;
            while (true)
            {
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                SelectLowestScoreServer(ChongqingServerList);
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                SelectLowestScoreServer(TianjinServerList);
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                SelectLowestScoreServer(GuangzhouServerList);
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                SelectLowestScoreServer(NanjingServerList);
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                Task.Delay(UPDATE_INTERVAL).Wait();
            }
        }

        public RelayCommand GroupButtonCommand { get; set; }
        private void ExecuteGroupButtonCommand()
        {
            var selectedServer = ChongqingServerList
                .Where(s => s.IsSelected)
                .FirstOrDefault();
            if (selectedServer != null)
            {
                ApplySelectedServer(selectedServer.IPAddress, "ds-cq-1.klbq.qq.com");
            }

            selectedServer = TianjinServerList
                .Where(s => s.IsSelected)
                .FirstOrDefault();
            if (selectedServer != null)
            {
                ApplySelectedServer(selectedServer.IPAddress, "ds-tj-1.klbq.qq.com");
            }

            selectedServer = GuangzhouServerList
                .Where(s => s.IsSelected)
                .FirstOrDefault();
            if (selectedServer != null)
            {
                ApplySelectedServer(selectedServer.IPAddress, "ds-gz-1.klbq.qq.com");
            }

            selectedServer = NanjingServerList
                .Where(s => s.IsSelected)
                .FirstOrDefault();
            if (selectedServer != null)
            {
                ApplySelectedServer(selectedServer.IPAddress, "ds-nj-1.klbq.qq.com");
            }
        }

        private static void ApplySelectedServer(string ipAddress, string domain)
        {
            HostsManager.Instance.ChangeDomain(ipAddress, domain);
        }

        private static void SelectLowestScoreServer(List<ServerInfo> serverInfoList)
        {
            var lowestScoreServer = serverInfoList
                .Where(s => s.Ping.Score >= 0)
                .OrderBy(s => s.Ping.Score).FirstOrDefault();

            if (lowestScoreServer != null)
            {
                foreach (var server in serverInfoList)
                {
                    server.IsSelected = server == lowestScoreServer;
                }
                ApplySelectedServer(lowestScoreServer.IPAddress, lowestScoreServer.Domain);
            }
        }
    }
}
