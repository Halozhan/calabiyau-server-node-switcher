using Core.Node;
using System.Collections.ObjectModel;
using System.Net;

namespace WpfApp.ViewModels
{
    public class DesignTimeNodeListViewModel : INodeListViewModel
    {
        public ObservableCollection<NodeViewModel> NodeList { get; set; }
        public int NodeCount => NodeList.Count;

        public DesignTimeNodeListViewModel()
        {
            NodeList = [];
            AddNode(new Node(IPAddress.Parse("43.155.138.82"), 20000));
            AddNode(new Node(IPAddress.Parse("43.128.155.169"), 20000));
        }

        public void AddNode(Node node)
        {
            // Invoke the UI thread to add the node
            App.Current.Dispatcher.Invoke(() =>
            {
                NodeList.Add(new NodeViewModel(node, NodeCount + 1));
            });
        }
    }
}
