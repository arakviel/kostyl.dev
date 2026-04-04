using Avalonia.Controls;

namespace AvaloniaHost.Views;

public partial class MainView : UserControl
{
    public static MainView? Instance { get; private set; }

    public MainView()
    {
        InitializeComponent();
        Instance = this;
    }
}