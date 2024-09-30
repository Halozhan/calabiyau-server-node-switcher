using CommunityToolkit.Mvvm.ComponentModel;

namespace CalabiyauServerNodeSwitcher.Models
{
    public class ServerInfo : ObservableObject
    {
        private string ipAddress;
        private Ping ping;
        private bool? vpn;

        public string IPAddress
        {
            get => ipAddress;
            set => SetProperty(ref ipAddress, value);
        }

        public Ping Ping
        {
            get => ping;
            set => SetProperty(ref ping, value);
        }

        public bool? VPN
        {
            get => vpn;
            set => SetProperty(ref vpn, value);
        }
    }
}
