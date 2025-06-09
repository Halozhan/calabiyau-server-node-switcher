using Microsoft.VisualStudio.TestTools.UnitTesting;
using Core.HostsManager;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.HostsManager.Tests
{
    [TestClass()]
    public class HostsManagerTests
    {
        private HostsManager hostsManager;
        private MockHostsFileHandler mockFileHandler;

        [TestInitialize]
        public void Initialize()
        {
            mockFileHandler = new MockHostsFileHandler();
            hostsManager = HostsManager.CreateForTesting(mockFileHandler);

        }

        [TestMethod()]
        public void GetInstanceTest()
        {
            // Act
            var instance1 = HostsManager.GetInstance();
            var instance2 = HostsManager.GetInstance();

            // Assert
            Assert.IsNotNull(instance1);
            Assert.AreSame(instance1, instance2); // 싱글톤이므로 동일한 인스턴스여야 함
        }

        [TestMethod()]
        public void LoadHostsTest()
        {
            // Arrange
            mockFileHandler.SetMockData(new[] { "127.0.0.1 localhost", "192.168.1.1 example.com" });

            // Act
            hostsManager.LoadHosts();

            // Assert
            Assert.AreEqual("127.0.0.1", hostsManager.GetIPByDomain("localhost"));
            Assert.AreEqual("192.168.1.1", hostsManager.GetIPByDomain("example.com"));
        }

        [TestMethod()]
        public void GetIPByDomainTest()
        {
            // Arrange
            mockFileHandler.SetMockData(new[] { "127.0.0.1 localhost", "192.168.1.1 example.com" });
            hostsManager.LoadHosts();

            // Act
            var ip1 = hostsManager.GetIPByDomain("localhost");
            var ip2 = hostsManager.GetIPByDomain("example.com");
            var ip3 = hostsManager.GetIPByDomain("nonexistent.com");

            // Assert
            Assert.AreEqual("127.0.0.1", ip1);
            Assert.AreEqual("192.168.1.1", ip2);
            Assert.IsNull(ip3); // 존재하지 않는 도메인은 null이어야 함
        }

        [TestMethod()]
        public void AddOrChangeHostTest()
        {
            // Arrange
            mockFileHandler.SetMockData(new[] { "127.0.0.1 localhost" });
            hostsManager.LoadHosts();
            var newHost = new Host("192.168.1.1", "example.com");

            // Act
            hostsManager.AddOrChangeHost(newHost);
            hostsManager.UpdateHostsFile();

            // Assert
            Assert.AreEqual("192.168.1.1", hostsManager.GetIPByDomain("example.com"));
            CollectionAssert.Contains(mockFileHandler.GetWrittenData(), "192.168.1.1\texample.com");
        }

        [TestMethod()]
        public void RemoveHostByDomainTest()
        {
            // Arrange
            mockFileHandler.SetMockData(new[] { "127.0.0.1 localhost", "192.168.1.1 example.com" });
            hostsManager.LoadHosts();

            // Act
            hostsManager.RemoveHostByDomain("example.com");
            hostsManager.UpdateHostsFile();

            // Assert
            Assert.IsNull(hostsManager.GetIPByDomain("example.com"));
            CollectionAssert.DoesNotContain(mockFileHandler.GetWrittenData(), "192.168.1.1 example.com");
        }

        [TestMethod()]
        public void UpdateHostsFileTest()
        {
            // Arrange
            mockFileHandler.SetMockData(new[] { "127.0.0.1 localhost" });
            hostsManager.LoadHosts();
            var newHost = new Host("192.168.1.1", "example.com");
            hostsManager.AddOrChangeHost(newHost);

            // Act
            hostsManager.UpdateHostsFile();

            // Assert
            var writtenData = mockFileHandler.GetWrittenData();
            CollectionAssert.Contains(writtenData, "127.0.0.1\tlocalhost");
            CollectionAssert.Contains(writtenData, "192.168.1.1\texample.com");
        }
    }

    // Mock 구현
    public class MockHostsFileHandler : IHostsFileHandler
    {
        private List<string> mockData = new();

        public void SetMockData(string[] data)
        {
            mockData = new List<string>(data);
        }

        public string[] ReadHosts()
        {
            return mockData.ToArray();
        }

        public void WriteHosts(string[] lines)
        {
            mockData = new List<string>(lines);
        }

        public string[] GetWrittenData()
        {
            return mockData.ToArray();
        }
    }
}