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
    public class HostsFileHandlerTests
    {
        private HostsFileHandler? hostsFileHandler;

        [TestInitialize]
        public void Initialize()
        {
            hostsFileHandler = HostsFileHandler.GetInstance();
        }

        [TestMethod()]
        public void GetInstanceTest()
        {
            // Act
            var instance = HostsFileHandler.GetInstance();

            // Assert
            Assert.IsNotNull(instance);
            Assert.AreSame(hostsFileHandler, instance);
        }

        [TestMethod()]
        public void SetHostsPathTest()
        {
            // Arrange
            string testPath = @"hostsTest";

            // Act
            hostsFileHandler.SetHostsPath(testPath);

            // Assert
            // Private field access for testing purposes
            // 테스트 목적으로 private 필드에 접근
            var field = typeof(HostsFileHandler).GetField("hostsPath", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            string actualPath = (string)field.GetValue(hostsFileHandler);
            Assert.AreEqual(testPath, actualPath);
        }

        [TestMethod()]
        public void ReadHostsTest()
        {
            // Arrange
            string testPath = @"hostsTest";
            hostsFileHandler.SetHostsPath(testPath);
            // 미리 hostsTest 파일을 생성하고 내용을 작성합니다.
            string[] expectedLines = { "127.0.0.1 localhost", "192.168.1.1 example.com" };
            File.WriteAllLines(testPath, expectedLines);

            // Act
            string[] actualLines = hostsFileHandler.ReadHosts();

            // Assert
            CollectionAssert.AreEqual(expectedLines, actualLines);
        }

        [TestMethod()]
        public void WriteHostsTest()
        {
            // Arrange
            string testPath = @"hostsTest";
            hostsFileHandler.SetHostsPath(testPath);
            string[] linesToWrite = { "127.0.0.1 localhost", "192.168.1.1 example.com" };

            // Act
            hostsFileHandler.WriteHosts(linesToWrite);

            // Assert
            string[] actualLines = File.ReadAllLines(testPath);
            CollectionAssert.AreEqual(linesToWrite, actualLines);
        }

        [TestCleanup]
        public void Cleanup()
        {
            // Clean up the test file if it exists
            string testPath = @"hostsTest";
            if (File.Exists(testPath))
            {
                File.Delete(testPath);
            }
        }
    }
}