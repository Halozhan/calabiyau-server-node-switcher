using Microsoft.VisualStudio.TestTools.UnitTesting;
using Core.LatencyChecker;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;

namespace Core.LatencyChecker.Tests
{
    [TestClass()]
    public class UDPSessionTests
    {
        [TestMethod()]
        public async Task UDPSessionTest()
        {
            // Arrange
            var address = IPAddress.Parse("43.155.193.230");
            var port = 20000;
            var latency = new List<float>();

            async Task LatencyAppend(float value)
            {
                latency.Add(value);
                await Task.CompletedTask;
            }

            var udpSession = new UDPSession(address, port, LatencyAppend);

            // Act
            udpSession.Start();
            await Task.Delay(5000);
            udpSession.Stop();

            // Assert
            Assert.IsTrue(latency.Average() > 0, "Average latency should be greater than 0.");
            Assert.IsTrue(latency.Average() < 1000, "Average latency should be less than 1000.");
        }
    }
}