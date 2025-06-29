using System.Collections.ObjectModel;
using WpfApp.Services;

namespace WpfApp.ViewModels
{
    public class DesignTimeMainWindowViewModel : IMainWindowViewModel
    {
        private readonly ObservableCollection<RegionViewModel> _regions;
        public IEnumerable<RegionViewModel> Regions => _regions;
        public readonly IRegionService _regionService;

        public DesignTimeMainWindowViewModel()
        {
            _regions = [];
            _regionService = new DesignTimeRegionService(_regions);
        }
    }
}
