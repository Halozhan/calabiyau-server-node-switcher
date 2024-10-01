using CommunityToolkit.Mvvm.ComponentModel;

namespace CalabiyauServerNodeSwitcher.Models
{
    public class ServerInfo : ObservableObject
    {
        private string ipAddress;
        private Ping ping;
        private bool isSelected;

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

        public bool IsSelected
        {
            get => isSelected;
            set => SetProperty(ref isSelected, value);
        }
    }
}
