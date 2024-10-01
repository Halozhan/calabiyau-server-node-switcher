using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace CalabiyauServerNodeSwitcher.Services
{
    public class HostsManager
    {
        private string hostsPath;

        public HostsManager()
        {
            this.hostsPath = @"C:\Windows\System32\drivers\etc\hosts";
        }

        public HostsManager(string hostsPath)
        {
            this.hostsPath = hostsPath;
        }

        public bool HasDomain(string domain)
        {
            string[] lines = System.IO.File.ReadAllLines(hostsPath);
            foreach (string line in lines)
            {
                if (line.Contains(domain))
                {
                    return true;
                }
            }
            return false;
        }

        public string GetIPAddress(string domain)
        {
            if (HasDomain(domain))
            {
                string[] lines = System.IO.File.ReadAllLines(hostsPath);
                foreach (string line in lines)
                {
                    if (line.Contains(domain))
                    {
                        return line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries)[0];
                    }
                }
            }
            return "";
        }

        public void AddDomain(string domain, string ipAddress)
        {
            if (!HasDomain(domain))
            {
                string[] lines = System.IO.File.ReadAllLines(hostsPath);
                List<string> newLines = new List<string>();
                foreach (string line in lines)
                {
                    newLines.Add(line);
                }
                newLines.Add(ipAddress + " " + domain);
                System.IO.File.WriteAllLines(hostsPath, newLines);
            }
        }

        public void RemoveDomain(string domain)
        {
            if (HasDomain(domain))
            {
                string[] lines = System.IO.File.ReadAllLines(hostsPath);
                List<string> newLines = new List<string>();
                foreach (string line in lines)
                {
                    if (!line.Contains(domain))
                    {
                        newLines.Add(line);
                    }
                }
                System.IO.File.WriteAllLines(hostsPath, newLines);
            }
        }

        public void ChangeDomain(string domain, string ipAddress)
        {
            if (HasDomain(domain))
            {
                RemoveDomain(domain);
            }
            AddDomain(domain, ipAddress);
        }
    }
}
