using System;
using System.Runtime.InteropServices.JavaScript;
using System.Runtime.Versioning;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Browser;
using Avalonia.Markup.Xaml;
using Avalonia.Controls;
using Avalonia.Styling;
using Avalonia.Media;
using AvaloniaHost;

[assembly: SupportedOSPlatform("browser")]

public partial class KostylBridge
{
    [JSImport("logToVue", "main.js")]
    internal static partial void LogToVue(string message);

    [JSExport]
    public static void UpdateXaml(string xaml)
    {
        try
        {
            var content = AvaloniaRuntimeXamlLoader.Parse<object>(xaml);
            Avalonia.Threading.Dispatcher.UIThread.Post(() =>
            {
                if (global::AvaloniaHost.Views.MainView.Instance != null)
                {
                    global::AvaloniaHost.Views.MainView.Instance.Content = content;
                    
                    // Connect the ViewModel to our logging bridge
                    if (global::AvaloniaHost.ViewModels.MainViewModel.Instance != null)
                    {
                        global::AvaloniaHost.ViewModels.MainViewModel.Instance.OnMessageAction = (msg) => 
                        {
                            LogToVue(msg);
                        };
                    }

                    LogToVue("XAML updated successfully.");
                }
            });
        }
        catch (Exception ex)
        {
            Avalonia.Threading.Dispatcher.UIThread.Post(() =>
            {
                if (global::AvaloniaHost.Views.MainView.Instance != null)
                {
                    global::AvaloniaHost.Views.MainView.Instance.Content = new TextBlock 
                    { 
                        Text = "XAML Error: " + ex.Message, 
                        Foreground = Avalonia.Media.Brushes.Red,
                        Margin = new Thickness(10),
                        TextWrapping = Avalonia.Media.TextWrapping.Wrap
                    };
                }
            });
        }
    }

    [JSExport]
    public static void SetTheme(string themeVariant)
    {
        Avalonia.Threading.Dispatcher.UIThread.Post(() =>
        {
            if (Application.Current != null)
            {
                Application.Current.RequestedThemeVariant = themeVariant.ToLower() switch
                {
                    "dark" => ThemeVariant.Dark,
                    "light" => ThemeVariant.Light,
                    _ => ThemeVariant.Default
                };
            }
        });
    }
}

internal sealed partial class Program
{
    private static Task Main(string[] args) => BuildAvaloniaApp()
            .StartBrowserAppAsync("out");

    public static AppBuilder BuildAvaloniaApp()
        => AppBuilder.Configure<App>()
            .With(new FontManagerOptions
            {
                DefaultFamilyName = "avares://AvaloniaHost/Assets/Fonts#Segoe UI"
            });
}