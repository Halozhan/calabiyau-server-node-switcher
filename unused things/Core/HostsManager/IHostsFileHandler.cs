using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.HostsManager
{
    public interface IHostsFileHandler
    {
        /// <summary>
        /// Reads all lines from the hosts file.
        /// </summary>
        /// <returns>An array of strings representing the lines in the hosts file.</returns>
        string[] ReadHosts();

        /// <summary>
        /// Writes the specified lines to the hosts file.
        /// </summary>
        /// <param name="lines">The lines to write to the file.</param>
        void WriteHosts(string[] lines);
    }
}
