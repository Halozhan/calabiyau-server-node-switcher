using CommunityToolkit.Mvvm.ComponentModel;

namespace CalabiyauServerNodeSwitcher.Models
{
    public class ServerInfo : ObservableObject
    {
        private string ipAddress;
        public string IPAddress
        {
            get => ipAddress;
            set => SetProperty(ref ipAddress, value);
        }

        private Ping ping;
        public Ping Ping
        {
            get => ping;
            set => SetProperty(ref ping, value);
        }

        private bool isSelected;
        public bool IsSelected
        {
            get => isSelected;
            set => SetProperty(ref isSelected, value);
        }

        private string domain;
        public string Domain
        {
            get => domain;
            set => SetProperty(ref domain, value);
        }
    }
}
