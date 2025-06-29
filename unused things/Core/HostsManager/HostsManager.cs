using System.Diagnostics;

namespace Core.HostsManager
{
    public sealed class HostsManager
    {
        private static readonly Lazy<HostsManager> instance = new(() => new HostsManager(HostsFileHandler.GetInstance()));

        private List<(string line, Host? host)> hostsList = [];
        private static readonly object hostsListLock = new();
        private readonly IHostsFileHandler fileHandler;

        // 기본 생성자 (싱글톤에서 사용)
        private HostsManager(IHostsFileHandler fileHandler)
        {
            this.fileHandler = fileHandler;
        }

        // Singleton pattern
        public static HostsManager Instance
        {
            get
            {
                return instance.Value;
            }
        }

        public static HostsManager GetInstance()
        {
            return instance.Value;
        }

        // 테스트용 팩토리 메서드
        public static HostsManager CreateForTesting(IHostsFileHandler mockFileHandler)
        {
            return new HostsManager(mockFileHandler);
        }

        public void LoadHosts()
        {
            lock (hostsListLock)
            {
                var readLine = fileHandler.ReadHosts();
                hostsList = HostsParser.ParseTextToHostsList(readLine);
            }
        }

        public string? GetIPByDomain(string domain)
        {
            lock (hostsListLock)
            {
                foreach (var (line, host) in hostsList)
                {
                    if (host?.Hostname == domain)
                    {
                        return host.IP;
                    }
                }
                return null;
            }
        }

        public void AddOrChangeHost(Host host)
        {
            lock (hostsListLock)
            {
                foreach (var (_, compareHost) in hostsList)
                {
                    if (compareHost?.Hostname == host.Hostname)
                    {
                        compareHost.IP = host.IP;
                        return;
                    }
                }
                hostsList.Add(("", host));
            }
        }

        public void RemoveHostByDomain(string domain)
        {
            lock (hostsListLock)
            {
                hostsList.RemoveAll(item => item.host?.Hostname == domain);
            }
        }

        public void UpdateHostsFile()
        {
            lock (hostsListLock)
            {
                var serializedLines = HostsParser.SerializeHostsListToText(hostsList);
                fileHandler.WriteHosts(serializedLines);
            }
        }
    }
}
