using System.Collections.ObjectModel;
using WpfApp.ViewModels;

namespace WpfApp.Services
{
    public class RegionService : IRegionService
    {
        private readonly ObservableCollection<RegionViewModel> _regions;
        private RegionFactory _regionFactory;

        public RegionService(ObservableCollection<RegionViewModel> regions)
        {
            _regions = regions;
            _regionFactory = new(_regions);

            Task.Run(() => LoadRegionsAsync());
        }

        public async Task LoadRegionsAsync()
        {
            var tasks = new[]
            {
                _regionFactory.LoadNodesAsync("成都, Chengdu", "cd"),
                _regionFactory.LoadNodesAsync("北京, Beijing", "bj"),
                _regionFactory.LoadNodesAsync("南京, Nanjing", "nj"),
                _regionFactory.LoadNodesAsync("广州, Guangzhou", "gz"),
            };

            await Task.WhenAll(tasks);
        }
    }
}
