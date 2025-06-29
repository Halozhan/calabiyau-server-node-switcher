using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.ObjectModel;
using WpfApp.Services;

namespace WpfApp.ViewModels
{
    public partial class MainWindowViewModel : ObservableObject, IMainWindowViewModel
    {
        private readonly ObservableCollection<RegionViewModel> _regions;
        public IEnumerable<RegionViewModel> Regions => _regions;
        private readonly IRegionService _regionService;

        public MainWindowViewModel()
        {
            _regions = [];
            _regionService = new RegionService(_regions);
        }
    }
}
