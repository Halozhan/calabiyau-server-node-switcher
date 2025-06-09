using System.Windows;
using WpfApp.ViewModels;
using WpfApp.Views;

namespace WpfApp
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            var mainWindow = new MainWindowView();
            var mainWindowViewModel = new MainWindowViewModel();

            mainWindow.DataContext = mainWindowViewModel;
            MainWindow = mainWindow;
            MainWindow.Show();
        }
    }
}
