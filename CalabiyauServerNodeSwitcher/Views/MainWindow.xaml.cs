using System.Windows;
using System.Windows.Controls;

namespace CalabiyauServerNodeSwitcher.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
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
