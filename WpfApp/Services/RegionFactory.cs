using DnsClient;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Net;
using WpfApp.ViewModels;

namespace WpfApp.Services
{
    public class RegionFactory
    {
        private readonly ObservableCollection<RegionViewModel> _regions;
        private IPEndPoint _endPoint;
        private LookupClient _client;
        public RegionFactory(ObservableCollection<RegionViewModel> regions)
        {
            _regions = regions;
            _endPoint = new IPEndPoint(IPAddress.Parse("1.1.1.1"), 53);
            _client = new LookupClient(_endPoint);
        }

        public async Task LoadNodesAsync(string regionName, string regionCode)
        {
            RegionViewModel regionViewModel = new(regionName, regionCode);

            // UI 스레드에서 Regions 컬렉션을 업데이트
            await App.Current.Dispatcher.InvokeAsync(() =>
            {
                _regions.Add(regionViewModel);
            });

            // EdgeOne Accelerator
            var edgeOneResult = await _client.QueryAsync($"klbqcp-prod-ds-{regionCode}1-eo.gxpan.cn", QueryType.A);
            var edgeOneResponse = edgeOneResult.Answers.ARecords();
            foreach (var record in edgeOneResponse)
            {
                var ip = record.Address;
                var port = 20000;
                Debug.WriteLine($"{regionName}.{regionCode}:EdgeOne Accelerator: {ip}");
                //regionViewModel.EdgeOne.AddNode(new(ip, port));
            }

            // Servers
            for (int i = 1; i <= 150; i++)
            {
                var serverResult = await _client.QueryAsync($"klbqcp-prod-ds-{regionCode}{i}-server.gxpan.cn", QueryType.A);
                var serverResponse = serverResult.Answers.ARecords();
                if (serverResponse.Count() == 0)
                {
                    break;
                }
                foreach (var record in serverResponse)
                {
                    var ip = record.Address;
                    var port = 20000;
                    Debug.WriteLine($"{regionName}.{regionCode}:{i}번째 Server: {ip}");
                    regionViewModel.Server.AddNode(new(ip, port));
                }
            }
        }
    }
}
