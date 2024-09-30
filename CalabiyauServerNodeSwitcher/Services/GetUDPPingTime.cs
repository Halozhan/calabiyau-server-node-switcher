using System.Diagnostics;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text;

namespace CalabiyauServerNodeSwitcher.Services
{
    public class GetUDPPingTime
    {
        private string ipAddress;
        private int port;

        private UdpClient udpClient;
        private const int TIMEOUT = 1000; // 1초 타임아웃
        private IPEndPoint remoteEndPoint;
        private byte[] sendBytes;
        private byte[] receiveBytes;

        public GetUDPPingTime(string ipAddress, int port)
        {
            this.ipAddress = ipAddress;
            this.port = port;
            udpClient = new UdpClient();

            remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
            sendBytes = Encoding.ASCII.GetBytes("a");
        }

        public float QueryPing()
        {
            float ping = -1;

            try
            {
                udpClient.Connect(ipAddress, port);
                udpClient.Client.ReceiveTimeout = TIMEOUT; // 1초 타임아웃 설정

                Stopwatch stopwatch = new Stopwatch();

                stopwatch.Start();
                udpClient.Send(sendBytes, sendBytes.Length);

                receiveBytes = udpClient.Receive(ref remoteEndPoint);
                stopwatch.Stop();

                ping = stopwatch.ElapsedTicks / (float)Stopwatch.Frequency * 1000;
            }
            catch (SocketException e)
            {
                Console.WriteLine(e.ToString());
            }
            catch (PingException e)
            {
                Console.WriteLine(e.ToString());
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

            return ping;
        }

        public async Task<float> AsyncQueryPing()
        {
            return await Task.Run(() => QueryPing());
        }

        public void Close()
        {
            udpClient.Close();
        }
    }
}
