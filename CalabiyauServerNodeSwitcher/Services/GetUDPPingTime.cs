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
        private const int TIMEOUT = 1000; // 1초 타임아웃
        private IPEndPoint remoteEndPoint;
        private byte[] sendBytes;
        private byte[] receiveBytes;
        private object lockObject = new object();
        private UdpClient udpClient;

        public GetUDPPingTime(string ipAddress, int port)
        {
            this.ipAddress = ipAddress;
            this.port = port;
            remoteEndPoint = new IPEndPoint(IPAddress.Parse(ipAddress), port);
            sendBytes = Encoding.ASCII.GetBytes("a");

            CreateClient();
        }

        public void CreateClient()
        {
            lock (lockObject)
            {
                if (udpClient != null)
                {
                    ClientClose();
                }

                udpClient = new UdpClient();
                udpClient.Client.ReceiveTimeout = TIMEOUT; // 1초 타임아웃 설정
                udpClient.Connect(remoteEndPoint);
            }
        }

        public void ClientClose()
        {
            lock (lockObject)
            {
                if (udpClient != null)
                {
                    udpClient.Close();
                    udpClient.Dispose();
                    udpClient = null;
                }
            }
        }

        public void ReEstablishConnection()
        {
            ClientClose();
            CreateClient();
        }

        public float QueryPing()
        {
            float ping = -1;

            if (udpClient == null)
            {
                CreateClient();
            }

            try
            {
                udpClient.Connect(remoteEndPoint);

                Stopwatch stopwatch = new Stopwatch();
                stopwatch.Reset();
                stopwatch.Start();
                udpClient.Send(sendBytes, sendBytes.Length);

                receiveBytes = udpClient.Receive(ref remoteEndPoint);
                stopwatch.Stop();

                // 보낸 값과 받은 값이 같은지 확인
                if (Encoding.ASCII.GetString(receiveBytes) != Encoding.ASCII.GetString(sendBytes))
                {
                    throw new Exception("wrong value");
                }

                ping = stopwatch.ElapsedTicks / (float)Stopwatch.Frequency * 1000;
            }
            catch (SocketException e)
            {
                if (e.SocketErrorCode == SocketError.TimedOut)
                {
                    // 타임아웃
                    //Trace.WriteLine(ipAddress + ": Timed out");
                }
                else
                {
                    Trace.WriteLine("Error pinging server " + ipAddress + ": " + e.SocketErrorCode + " " + e.Message);
                }
            }
            catch (PingException)
            {
                // 핑이 너무 높아서 응답이 없을 때
            }
            catch (Exception e)
            {
                // 그 외의 예외
                Trace.TraceError("Error pinging server " + ipAddress + ": " + e.Message);
            }


            return ping;
        }
    }
}
