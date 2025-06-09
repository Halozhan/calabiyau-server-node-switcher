using Core.Node;
using System.Collections.ObjectModel;

namespace WpfApp.ViewModels
{
    public class NodeListViewModel : INodeListViewModel
    {
        public ObservableCollection<NodeViewModel> NodeList { get; set; }
        public int NodeCount => NodeList.Count;

        public NodeListViewModel()
        {
            NodeList = [];
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
