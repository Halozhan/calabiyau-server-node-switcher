using CalabiyauServerNodeSwitcher.Models;
using CalabiyauServerNodeSwitcher.Services;
using System.Windows;
using System.Windows.Controls;

namespace CalabiyauServerNodeSwitcher.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            List<ServerInfo> tianjin = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "109.244.173.239", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "109.244.173.251", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "111.30.170.175", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "111.33.110.226", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "116.130.228.105", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "116.130.229.177", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "123.151.54.47", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "42.81.194.60", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.159.233.14", Ping = new Ping(), VPN = false }
            };
            tianjin_servers.ItemsSource = tianjin;

            List<ServerInfo> nanjing = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "112.80.183.27", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "121.229.92.16", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "180.110.193.185", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "182.50.15.118", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "36.155.164.82", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "36.155.183.208", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.141.129.109", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.141.129.21", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.159.233.198", Ping = new Ping(), VPN = false }
            };
            nanjing_servers.ItemsSource = nanjing;

            List<ServerInfo> guangzhou = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "120.232.24.96", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "120.233.18.175", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "14.29.103.46", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "157.148.58.53", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "157.255.4.48", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "183.47.107.193", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.139.252.183", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.141.58.200", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.159.233.178", Ping = new Ping(), VPN = false }
            };
            guangzhou_servers.ItemsSource = guangzhou;

            List<ServerInfo> chongqing = new List<ServerInfo>
            {
                new ServerInfo { IPAddress = "111.10.11.250", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "111.10.11.73", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "113.250.9.54", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "113.250.9.56", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "175.27.48.249", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "175.27.49.194", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "43.159.233.98", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "58.144.164.43", Ping = new Ping(), VPN = false },
                new ServerInfo { IPAddress = "58.144.164.50", Ping = new Ping(), VPN = false }
            };
            chongqing_servers.ItemsSource = chongqing;

            // Thread
            Thread pingThread = new Thread(StartQueryPing);
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
                    thread.Start();
                }
            }
        }

        private async void QueryThread(ServerInfo serverInfo)
        {
            const int PingInterval = 1000 / 100;
            const int port = 6001;
            var udpClient = new GetUDPPingTime(serverInfo.IPAddress, port);

            while (true)
            {
                try
                {
                    // 핑값을 측정하여 추가
                    float latency = udpClient.QueryPing();
                    serverInfo.Ping.AddPing = latency;
                }
                catch (IndexOutOfRangeException ex)
                {
                    // 예외 처리: 로그를 남기거나 사용자에게 알림
                    Console.WriteLine($"Error pinging server {serverInfo.IPAddress}: {ex.Message}");
                }
                catch (Exception ex)
                {
                    // 예외 처리: 로그를 남기거나 사용자에게 알림
                    Console.WriteLine($"Error pinging server {serverInfo.IPAddress}: {ex.Message}");
                }

                await Task.Delay(PingInterval);
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
    }
}
