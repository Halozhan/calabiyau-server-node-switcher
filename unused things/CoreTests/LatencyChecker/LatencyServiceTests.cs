using Microsoft.VisualStudio.TestTools.UnitTesting;
using Core.LatencyChecker;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.LatencyChecker.Tests
{
    [TestClass()]
    public class LatencyServiceTests
    {
        [TestMethod()]
        public void UpdateTest_WithValidLatencies()
        {
            // Arrange
            var latency = new Latency();
            latency.Add(50);
            latency.Add(100);
            latency.Add(200);
            var latencyService = new LatencyService(latency);

            // Act
            latencyService.Update();

            // Assert
            Assert.AreEqual(3, latencyService.RemovedOutlier.Count);
            Assert.AreEqual(50, latencyService.Min);
            Assert.AreEqual(200, latencyService.Max);
            Assert.AreEqual(116.67f, latencyService.Average, 0.01f); // Allowing small precision error
            Assert.AreEqual(0, latencyService.LossRate);
            Assert.IsTrue(latencyService.StandardDeviation > 0);
            Assert.IsTrue(latencyService.Score > 0);
        }

        [TestMethod()]
        public void UpdateTest_WithOutliers()
        {
            // Arrange
            var latency = new Latency();
            latency.Add(-10); // Invalid latency
            latency.Add(50);
            latency.Add(1500); // Outlier
            latency.Add(100);
            var latencyService = new LatencyService(latency);

            // Act
            latencyService.Update();

            // Assert
            Assert.AreEqual(2, latencyService.RemovedOutlier.Count); // Only valid latencies remain
            Assert.AreEqual(50, latencyService.Min);
            Assert.AreEqual(100, latencyService.Max);
            Assert.AreEqual(75, latencyService.Average);
            Assert.AreEqual(0, latencyService.LossRate);
        }

        [TestMethod()]
        public void UpdateTest_WithLossRate()
        {
            // Arrange
            var latency = new Latency();
            latency.Add(-1); // Packet loss
            latency.Add(100);
            latency.Add(-1); // Packet loss
            latency.Add(200);
            var latencyService = new LatencyService(latency);

            // Act
            latencyService.Update();

            // Assert
            Assert.AreEqual(2, latencyService.RemovedOutlier.Count); // Only valid latencies remain
            Assert.AreEqual(100, latencyService.Min);
            Assert.AreEqual(200, latencyService.Max);
            Assert.AreEqual(150, latencyService.Average);
            Assert.AreEqual(0.5f, latencyService.LossRate); // 50% loss rate
        }

        [TestMethod()]
        public void UpdateTest_WithEmptyLatencies()
        {
            // Arrange
            var latency = new Latency();
            var latencyService = new LatencyService(latency);

            // Act
            latencyService.Update();

            // Assert
            Assert.AreEqual(0, latencyService.RemovedOutlier.Count);
            Assert.AreEqual(-1, latencyService.Min);
            Assert.AreEqual(-1, latencyService.Max);
            Assert.AreEqual(-1, latencyService.Average);
            Assert.AreEqual(-1, latencyService.LossRate);
            Assert.AreEqual(-1, latencyService.StandardDeviation);
            Assert.AreEqual(-1, latencyService.Score);
        }
    }
}