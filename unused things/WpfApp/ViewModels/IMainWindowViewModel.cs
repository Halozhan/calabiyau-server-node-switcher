namespace WpfApp.ViewModels
{
    public interface IMainWindowViewModel
    {
        IEnumerable<RegionViewModel> Regions { get; }
    }
}
