namespace Core.HostsManager
{
    public class Host(string ip, string hostname)
    {
        public string IP { get; set; } = ip;
        public string Hostname { get; set; } = hostname;
    }
}
