using System.Net;

namespace Core.Node
{
    public class Node(IPAddress address, int port)
    {
        public IPAddress? IPAddress { get; set; } = address;
        public int Port { get; set; } = port;
    }
}
