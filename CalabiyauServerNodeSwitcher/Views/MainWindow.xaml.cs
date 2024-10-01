using CalabiyauServerNodeSwitcher.Models;
using CalabiyauServerNodeSwitcher.Services;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;

namespace CalabiyauServerNodeSwitcher.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            // tianjin
            List<ServerInfo> tianjin = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "109.244.173.239", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "109.244.173.251", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "111.30.170.175", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "111.33.110.226", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "116.130.228.105", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "116.130.229.177", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "123.151.54.47", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "42.81.194.60", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.159.233.14", Ping = new Ping(), IsSelected = false }
            };
            tianjin_servers.Items.Clear();
            tianjin_servers.ItemsSource = tianjin;

            string tianjinIP = new HostsManager().GetIPAddress("ds-tj-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in tianjin)
            {
                if (serverInfo.IPAddress == tianjinIP)
                {
                    serverInfo.IsSelected = true;
                }
            }


            // nanjing
            List<ServerInfo> nanjing = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "112.80.183.27", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "121.229.92.16", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "180.110.193.185", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "182.50.15.118", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "36.155.164.82", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "36.155.183.208", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.141.129.109", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.141.129.21", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.159.233.198", Ping = new Ping(), IsSelected = false }
            };
            nanjing_servers.Items.Clear();
            nanjing_servers.ItemsSource = nanjing;

            string nanjingIP = new HostsManager().GetIPAddress("ds-nj-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in nanjing)
            {
                if (serverInfo.IPAddress == nanjingIP)
                {
                    serverInfo.IsSelected = true;
                }
            }

            // guangzhou
            List<ServerInfo> guangzhou = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "120.232.24.96", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "120.233.18.175", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "14.29.103.46", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "157.148.58.53", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "157.255.4.48", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "183.47.107.193", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.139.252.183", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.141.58.200", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.159.233.178", Ping = new Ping(), IsSelected = false }
            };
            guangzhou_servers.Items.Clear();
            guangzhou_servers.ItemsSource = guangzhou;

            string guangzhouIP = new HostsManager().GetIPAddress("ds-gz-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in guangzhou)
            {
                if (serverInfo.IPAddress == guangzhouIP)
                {
                    serverInfo.IsSelected = true;
                }
            }


            // chongqing
            List<ServerInfo> chongqing = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "111.10.11.250", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "111.10.11.73", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "113.250.9.54", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "113.250.9.56", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "175.27.48.249", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "175.27.49.194", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "43.159.233.98", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "58.144.164.43", Ping = new Ping(), IsSelected = false },
                new ServerInfo { IPAddress = "58.144.164.50", Ping = new Ping(), IsSelected = false }
            };
            chongqing_servers.Items.Clear();
            chongqing_servers.ItemsSource = chongqing;

            string chongqingIP = new HostsManager().GetIPAddress("ds-cq-1.klbq.qq.com");

            foreach (ServerInfo serverInfo in chongqing)
            {
                if (serverInfo.IPAddress == chongqingIP)
                {
                    serverInfo.IsSelected = true;
                }
            }


            // Thread
            Thread pingThread = new Thread(StartQueryPing);
            pingThread.Name = "PingThread";
            pingThread.Start();
        }

        private async void StartQueryPing()
        {
            Dictionary<string, GetUDPPingTime> udpClient = new Dictionary<string, GetUDPPingTime>();

            var allServers = new List<List<ServerInfo>>
            {
                tianjin_servers.Items.Cast<ServerInfo>().ToList(),
                nanjing_servers.Items.Cast<ServerInfo>().ToList(),
                guangzhou_servers.Items.Cast<ServerInfo>().ToList(),
                chongqing_servers.Items.Cast<ServerInfo>().ToList()
            };

            foreach (var serverList in allServers)
            {
                foreach (ServerInfo serverInfo in serverList)
                {
                    Thread thread = new Thread(() => QueryThread(serverInfo));
                    thread.Name = serverInfo.IPAddress;
                    thread.Start();
                }
            }
        }

        private async void QueryThread(ServerInfo serverInfo)
        {
            const ushort SECOND = 1000;
            const ushort PACKET_PER_SECOND = 100;
            const uint REFRESH_INTERVAL = PACKET_PER_SECOND;
            const ushort PING_INTERVAL = SECOND / PACKET_PER_SECOND;
            const ushort PORT = 6001;
            var udpClient = new GetUDPPingTime(serverInfo.IPAddress, PORT);

            try
            {
                while (true)
                {
                    for (int i = 0; i < REFRESH_INTERVAL; i++)
                    {
                        // 핑값을 측정하여 추가
                        float latency = udpClient.QueryPing();
                        serverInfo.Ping.AddPing = latency;

                        // 핑 간격 보정
                        //int delay = PING_INTERVAL - (int)(latency * 1000);

                        //// 핑 간격이 0보다 작으면 0으로 설정
                        //if (delay < 0)
                        //{
                        //    delay = 0;
                        //}
                        await Task.Delay(PING_INTERVAL);
                    }
                    udpClient.ClientClose();
                }
            }
            catch (Exception ex)
            {
                // 예외 발생 시 스레드 이름과 예외 메시지 출력
                Trace.WriteLine($"Thread '{Thread.CurrentThread.Name}' has exited with an exception: {ex.Message}");
            }
            finally
            {
                // 스레드가 정상적으로 종료될 때 스레드 이름 출력
                Trace.WriteLine($"Thread '{Thread.CurrentThread.Name}' has exited.");
            }
        }

        private void CopyIPAddress(object sender, RoutedEventArgs e)
        {
            if (sender is MenuItem menuItem && menuItem.Parent is ContextMenu contextMenu && contextMenu.PlacementTarget is TextBox textBox)
            {
                try
                {
                    Dispatcher.Invoke(() => Clipboard.SetText(textBox.Text));
                }
                catch (System.Runtime.InteropServices.COMException)
                {
                    // Handle the exception, e.g., log it or show a message to the user
                    MessageBox.Show("Failed to copy text to clipboard. Please try again.", "Clipboard Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void TianjinButton_Click(object sender, RoutedEventArgs e)
        {
            ApplySelectedServer(tianjin_servers, "ds-tj-1.klbq.qq.com");
        }

        private void NanjingButton_Click(object sender, RoutedEventArgs e)
        {
            ApplySelectedServer(nanjing_servers, "ds-nj-1.klbq.qq.com");
        }

        private void ChongqingButton_Click(object sender, RoutedEventArgs e)
        {
            ApplySelectedServer(chongqing_servers, "ds-cq-1.klbq.qq.com");
        }

        private void GuangzhouButton_Click(object sender, RoutedEventArgs e)
        {
            ApplySelectedServer(guangzhou_servers, "ds-gz-1.klbq.qq.com");
        }

        private void ApplySelectedServer(ListView serverListView, string domain)
        {
            var selectedServer = serverListView.Items.Cast<ServerInfo>().FirstOrDefault(s => s.IsSelected);
            if (selectedServer != null)
            {
                new HostsManager().ChangeDomain(domain, selectedServer.IPAddress);
                MessageBox.Show($"Applied {selectedServer.IPAddress} to {domain}", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            else
            {
                MessageBox.Show("No server selected.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}
