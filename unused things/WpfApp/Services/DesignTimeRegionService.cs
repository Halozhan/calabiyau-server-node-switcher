using System.Collections.ObjectModel;
using WpfApp.ViewModels;

namespace WpfApp.Services
{
    public class DesignTimeRegionService : IRegionService
    {
        private readonly ObservableCollection<RegionViewModel> _regions;
        private RegionFactory _regionFactory;

        public DesignTimeRegionService(ObservableCollection<RegionViewModel> regions)
        {
            _regions = regions;
            _regionFactory = new(_regions);

            Task.Run(() => LoadRegionsAsync());
        }

        public async Task LoadRegionsAsync()
        {
            var tasks = new[]
            {
                _regionFactory.LoadNodesAsync("南京, Nanjing", "nj"),
                _regionFactory.LoadNodesAsync("广州, Guangzhou", "gz"),
            };

            await Task.WhenAll(tasks);
        }
    }
}
