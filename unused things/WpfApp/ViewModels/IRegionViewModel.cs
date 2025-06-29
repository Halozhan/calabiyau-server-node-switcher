namespace WpfApp.ViewModels
{
    public interface IRegionViewModel
    {
        string Name { get; set; }
        INodeListViewModel Server { get; set; }
        NodeViewModel WorstServer { get; }
        //INodeListViewModel EdgeOne { get; set; }
        //NodeViewModel BestEdgeOne { get; }
    }
}
