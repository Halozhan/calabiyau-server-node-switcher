using System.Net.Http;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;

namespace CalabiyauServerNodeSwitcher.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            CheckForUpdates();
        }

        private async void CheckForUpdates()
        {
            try
            {
                // Get the latest version from the GitHub repository
                HttpClient client = new HttpClient();
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, "https://github.com/Halozhan/calabiyau-server-node-switcher/releases/latest");
                HttpResponseMessage response = await client.SendAsync(request);
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException($"Request failed with status code {response.StatusCode}");
                }
                string responseUri = response.RequestMessage.RequestUri.ToString();
                string latestVersion = responseUri.Substring(responseUri.LastIndexOf('/') + 1);

                // Get the current version of the application
                Assembly assembly = Assembly.GetExecutingAssembly();
                string currentVersion = assembly.GetName().Version.ToString();

                // Split the versions into parts
                string[] latestVersionParts = latestVersion.Split('.');
                string[] currentVersionParts = currentVersion.Split('.');

                // Compare only the major, minor, and build versions (ignore the revision)
                if (latestVersionParts.Length >= 4)
                {
                    latestVersion = string.Join(".", latestVersionParts, 0, 3);
                }

                if (currentVersionParts.Length >= 4)
                {
                    currentVersion = string.Join(".", currentVersionParts, 0, 3);
                }

                // Compare the versions
                if (latestVersion != currentVersion)
                {
                    MessageBox.Show("A new version is available. Please update the application.", "Update Available", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
            catch (HttpRequestException)
            {
                // Handle the exception, e.g., log it or show a message to the user
                MessageBox.Show("Failed to check for updates. Please try again later.", "Update Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void CopyIPAddress(object sender, RoutedEventArgs e)
        {
            if (sender is MenuItem menuItem && menuItem.Parent is ContextMenu contextMenu && contextMenu.PlacementTarget is TextBox textBox)
            {
                try
                {
                    Dispatcher.Invoke(() => Clipboard.SetText(textBox.Text));
                }
                catch (System.Runtime.InteropServices.COMException)
                {
                    // Handle the exception, e.g., log it or show a message to the user
                    MessageBox.Show("Failed to copy text to clipboard. Please try again.", "Clipboard Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }
    }
}
