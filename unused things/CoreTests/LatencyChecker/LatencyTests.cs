using Microsoft.VisualStudio.TestTools.UnitTesting;
using Core.LatencyChecker;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Concurrent;

namespace Core.LatencyChecker.Tests
{
    [TestClass()]
    public class LatencyTests
    {
        [TestMethod()]
        public void LatencyTest()
        {
            
        }

        [TestMethod()]
        public void AddTest()
        {
            // Arrange
            var latency = new Latency();
            float ping = 100.5f;

            // Act
            latency.Add(ping);

            // Assert
            Assert.AreEqual(1, latency.GetLatencyList().Count);
            Assert.AreEqual(ping, latency.GetLatencyList().First());
        }

        [TestMethod()]
        public void ClearTest()
        {
            // Arrange
            var latency = new Latency();
            latency.Add(100.5f);
            latency.Add(200.5f);

            // Act
            latency.Clear();

            // Assert
            Assert.AreEqual(0, latency.GetLatencyList().Count);
        }

        [TestMethod()]
        public void GetLatencyListTest()
        {
            // Arrange
            var latency = new Latency();
            latency.Add(100.5f);
            latency.Add(200.5f);

            // Act
            ConcurrentQueue<float> latencyList = latency.GetLatencyList();

            // Assert
            Assert.AreEqual(2, latencyList.Count);
            Assert.IsTrue(latencyList.Contains(100.5f));
            Assert.IsTrue(latencyList.Contains(200.5f));
        }

        [TestMethod()]
        public void LatencyTest_MaxCapacity()
        {
            // Arrange
            var latency = new Latency();
            for (int i = 0; i < 250; i++)
            {
                latency.Add(i);
            }

            // Act
            var latencyList = latency.GetLatencyList();

            // Assert
            Assert.AreEqual(200, latencyList.Count); // MaxCapacity is 200
            Assert.IsFalse(latencyList.Contains(0)); // Oldest entries should be removed
            Assert.IsFalse(latencyList.Contains(49)); // 경계값 테스트
            Assert.IsTrue(latencyList.Contains(50)); // Entries from 50 to 249 should remain
        }
    }
}