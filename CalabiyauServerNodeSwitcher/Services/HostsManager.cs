using System.Diagnostics;
using System.IO;

namespace CalabiyauServerNodeSwitcher.Services
{
    public class HostsManager
    {
        private static HostsManager? instance;
        private static readonly object instanceLock = new object();
        private static readonly object fileLock = new object();
        private string hostsPath;

        // Private constructor to prevent instantiation
        private HostsManager()
        {
            this.hostsPath = @"C:\Windows\System32\drivers\etc\hosts";
        }

        // Public static method to get the singleton instance
        public static HostsManager Instance
        {
            get
            {
                lock (instanceLock)
                {
                    instance ??= new HostsManager();
                }
                return instance;
            }
        }

        // Optional: Overloaded method to set a custom hosts path
        public static HostsManager GetInstance(string hostsPath)
        {
            lock (instanceLock)
            {
                if (instance == null)
                {
                    instance = new HostsManager { hostsPath = hostsPath };
                }
            }
            return instance;
        }

        public bool HasDomain(string domain)
        {
            lock (fileLock)
            {
                try
                {
                    string[] lines = File.ReadAllLines(hostsPath);
                    foreach (string line in lines)
                    {
                        if (line.Contains(domain))
                        {
                            return true;
                        }
                    }
                }
                catch (IOException)
                {
                    return false;
                }
                return false;
            }
        }

        public string GetIPAddress(string domain)
        {
            lock (fileLock)
            {
                try
                {
                    string[] lines = File.ReadAllLines(hostsPath);
                    foreach (string line in lines)
                    {
                        if (line.Contains(domain))
                        {
                            return line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries)[0];
                        }
                    }
                }
                catch (IOException)
                {
                    return "";
                }
                return "";
            }
        }

        public void AddDomain(string domain, string ipAddress)
        {
            lock (fileLock)
            {
                if (!HasDomain(domain))
                {
                    try
                    {
                        string[] lines = File.ReadAllLines(hostsPath);
                        List<string> newLines = new List<string>(lines)
                        {
                            ipAddress + " " + domain
                        };
                        File.WriteAllLines(hostsPath, newLines);
                    }
                    catch (IOException e)
                    {
                        Trace.WriteLine("AddDomain: " + e);
                    }
                }
            }
        }

        public void RemoveDomain(string domain)
        {
            lock (fileLock)
            {
                bool success = false;
                int retries = 3;
                while (!success && retries > 0)
                {
                    try
                    {
                        string[] lines = File.ReadAllLines(hostsPath);
                        List<string> newLines = new List<string>();
                        foreach (string line in lines)
                        {
                            if (!line.Contains(domain))
                            {
                                newLines.Add(line);
                            }
                        }
                        File.WriteAllLines(hostsPath, newLines);
                        success = true;
                    }
                    catch (IOException)
                    {
                        retries--;
                        Task.Delay(100).Wait(); // Wait before retrying
                    }
                }
            }
        }

        public void ChangeDomain(string ipAddress, string domain)
        {
            lock (fileLock)
            {
                if (GetIPAddress(domain) == ipAddress)
                {
                    return;
                }
                if (HasDomain(domain))
                {
                    RemoveDomain(domain);
                }
                AddDomain(domain, ipAddress);
            }
        }
    }
}
