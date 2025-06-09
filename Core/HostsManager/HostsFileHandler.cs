using System.Diagnostics;

namespace Core.HostsManager
{
    public sealed class HostsFileHandler : IHostsFileHandler
    {
        private static readonly Lazy<HostsFileHandler> instance = new(() => new HostsFileHandler());
        private static readonly object fileLock = new();
        private string hostsPath = @"C:\Windows\System32\drivers\etc\hosts";

        private HostsFileHandler() { }

        // Singleton pattern
        public static HostsFileHandler Instance
        {
            get
            {
                return instance.Value;
            }
        }

        public static HostsFileHandler GetInstance()
        {
            return instance.Value;
        }

        public void SetHostsPath(string path)
        {
            lock (fileLock)
            {
                hostsPath = path;
            }
        }

        public string[] ReadHosts()
        {
            lock (fileLock)
            {
                try
                {
                    return File.ReadAllLines(hostsPath);
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(ex.Message);
                    throw new Exception("Error reading hosts file");
                }
            }
        }

        public void WriteHosts(string[] lines)
        {
            lock (fileLock)
            {
                try
                {
                    File.WriteAllLines(hostsPath, lines);
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(ex.Message);
                    throw new Exception("Error writing hosts file");
                }
            }
        }
    }
}
