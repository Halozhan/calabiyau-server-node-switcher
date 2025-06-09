using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Core.LatencyChecker
{
    public class UDPSession
    {
        private IPAddress _ipAddress;
        private int _port;

        private IPEndPoint _remoteEndPoint;
        private byte[] _sendBytes;

        private readonly CancellationTokenSource _cancellationTokenSource;
        private Thread _thread;

        public UDPSession(IPAddress address, int port, Func<float, Task> latencyAppend)
        {
            _ipAddress = address;
            _port = port;

            // 목적지
            _remoteEndPoint = new IPEndPoint(_ipAddress, _port);

            _cancellationTokenSource = new CancellationTokenSource();
            _thread = new Thread(() => RunAsync(_cancellationTokenSource.Token, latencyAppend).GetAwaiter().GetResult())
            {
                IsBackground = true
            };
        }

        private void SendData(UdpClient udpClient)
        {
            udpClient.Send(_sendBytes, _sendBytes.Length);
        }

        private byte[] ReceiveData(UdpClient udpClient)
        {
            return udpClient.Receive(ref _remoteEndPoint);
        }

        public async Task<byte[]> ReceiveDataAsync(UdpClient udpClient)
        {
            var receiveTask = udpClient.ReceiveAsync();
            await receiveTask;
            return receiveTask.Result.Buffer;
        }


        // Thread
        public void Start()
        {
            _thread.Start();
        }

        public void Stop()
        {
            _cancellationTokenSource.Cancel();
            _thread.Join();
        }

        // 취소 토큰과 삽입할 데이터의 콜백 함수를 받아서 실행
        private async Task RunAsync(CancellationToken token, Func<float, Task> latencyAppend)
        {
            Stopwatch stopwatch = new();

            while (!token.IsCancellationRequested)
            {
                using (UdpClient udpClient = new())
                {
                    int lossCountDuringSession = 0;
                    udpClient.Client.ReceiveTimeout = 1000; // 1초 타임아웃 설정
                    udpClient.Connect(_ipAddress, _port);
                    for (int i = 0; (i < 50) && !token.IsCancellationRequested; i++)
                    {
                        // 패킷 손실이 lossCountDuringSession 조건을 만족하면 재연결
                        if (lossCountDuringSession >= 10)
                        {
                            break;
                        }

                        try
                        {
                            // 보낼 패킷 랜덤 데이터
                            _sendBytes = Encoding.ASCII.GetBytes(new Random().Next().ToString());

                            // Send data
                            stopwatch.Restart();
                            SendData(udpClient);

                            // Receive data
                            byte[] receiveBytes = ReceiveData(udpClient);
                            stopwatch.Stop();

                            // 보낸 패킷과 받은 패킷이 같은지 확인
                            if (Encoding.ASCII.GetString(_sendBytes) != Encoding.ASCII.GetString(receiveBytes))
                            {
                                throw new Exception("Wrong packet received.");
                            }

                            // 핑이 1000ms 초과하면
                            if (stopwatch.ElapsedMilliseconds > 1000)
                            {
                                throw new Exception("Latency is over 1000ms.");
                            }

                            // Add latency to the list
                            await latencyAppend(stopwatch.ElapsedTicks / (float)Stopwatch.Frequency * 1000);
                        }
                        catch (Exception ex)
                        {
                            Debug.WriteLine($"Error during UDP session: {ex.Message}");
                            lossCountDuringSession++;
                            await latencyAppend(-1);
                            continue;
                        }
                        finally
                        {
                            stopwatch.Stop();

                            // Calculate delay
                            long elapsedMilliseconds = stopwatch.ElapsedMilliseconds;
                            if (elapsedMilliseconds < 200)
                            {
                                try
                                {
                                    await Task.Delay(200 - (int)elapsedMilliseconds, token);
                                }
                                catch (TaskCanceledException)
                                {
                                    // Handle the cancellation exception if needed
                                    Debug.WriteLine("Task was canceled.");
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
