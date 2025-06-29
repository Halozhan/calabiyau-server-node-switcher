using System.Collections.ObjectModel;

namespace Core.Region
{
    public class Region
    {
        public string Name { get; private set; }
        public ObservableCollection<Node.Node> Nodes { get; private set; }

        public Region(string name)
        {
            Name = name;
            Nodes = [];
        }

        public void Add(Node.Node node)
        {
            Nodes.Add(node);
        }
    }
}
