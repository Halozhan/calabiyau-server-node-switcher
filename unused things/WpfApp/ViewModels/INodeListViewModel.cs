using Core.Node;
using System.Collections.ObjectModel;

namespace WpfApp.ViewModels
{
    public interface INodeListViewModel
    {
        ObservableCollection<NodeViewModel> NodeList { get; set; }
        int NodeCount { get; }
        void AddNode(Node node);
    }
}
