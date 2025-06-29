using System.Net;

namespace WpfApp.ViewModels
{
    public class DesignTimeRegionViewModel : IRegionViewModel
    {
        public string Name { get; set; }
        public INodeListViewModel Server { get; set; }
        public NodeViewModel WorstServer => Server.NodeList.MaxBy(node => node.Latency.Score);
        public INodeListViewModel EdgeOne { get; set; }
        public NodeViewModel BestEdgeOne => EdgeOne.NodeList.MinBy(node => node.Latency.Score);

        public DesignTimeRegionViewModel()
        {
            Name = "Mock Region";
            Server = new NodeListViewModel();
            Server.AddNode(new(IPAddress.Parse("43.155.138.82"), 20000));
            EdgeOne = new NodeListViewModel();
            EdgeOne.AddNode(new(IPAddress.Parse("43.175.253.233"), 20000));
        }
    }
}
