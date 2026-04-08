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
using Avalonia.Controls.Primitives;
using AvaloniaHost;
using Avalonia.Media.Fonts;

[assembly: SupportedOSPlatform("browser")]

public partial class KostylBridge
{
    [JSImport("logToVue", "main.js")]
    internal static partial void LogToVue(string message);

    [JSImport("logErrorToVue", "main.js")]
    internal static partial void LogErrorToVue(string message, string xaml);

    [JSImport("setIframeHeight", "main.js")]
    internal static partial void SetIframeHeight(double height);

    [JSExport]
    public static void UpdateXaml(string xaml)
    {
        try
        {
            var content = AvaloniaRuntimeXamlLoader.Load(new RuntimeXamlLoaderDocument(xaml));
            
            Avalonia.Threading.Dispatcher.UIThread.Post(() =>
            {
                if (global::AvaloniaHost.Views.MainView.Instance != null)
                {
                    if (content is Avalonia.Controls.Control control)
                    {
                        // Ensure NameScope is present for ElementName bindings
                        if (NameScope.GetNameScope(control) == null)
                        {
                            NameScope.SetNameScope(control, new NameScope());
                        }

                        control.VerticalAlignment = Avalonia.Layout.VerticalAlignment.Top;
                        control.HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Stretch;

                        double lastHeight = 0;
                        global::AvaloniaHost.Views.MainView.Instance.LayoutUpdated += (s, e) => 
                        {
                            var h = control.Bounds.Height;
                            if (h <= 0) h = control.DesiredSize.Height;
                            
                            double totalHeight = Math.Ceiling(h + control.Margin.Top + control.Margin.Bottom + 32);
                            
                            if (Math.Abs(totalHeight - lastHeight) > 2)
                            {
                                lastHeight = totalHeight;
                                SetIframeHeight(totalHeight);
                            }
                        };

                        global::AvaloniaHost.Views.MainView.Instance.Content = control;
                    }
                    else
                    {
                        global::AvaloniaHost.Views.MainView.Instance.Content = content;
                    }

                    LogToVue("XAML updated successfully.");
                }
                else
                {
                    // MainView.Instance is null
                }
            });
        }
        catch (Exception ex)
        {
            Avalonia.Threading.Dispatcher.UIThread.Post(() =>
            {
                LogErrorToVue(ex.Message, xaml);
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

public sealed class MyFontCollection : EmbeddedFontCollection
{
    public MyFontCollection() : base(
        new Uri("fonts:MyFonts", UriKind.Absolute),
        new Uri("avares://AvaloniaHost/Assets/Fonts", UriKind.Absolute))
    {
    }
}

internal sealed partial class Program
{
    private static Task Main(string[] args) => BuildAvaloniaApp()
            .StartBrowserAppAsync("out");

    public static AppBuilder BuildAvaloniaApp()
    {
        // Force reference types to ensure they are loaded and not trimmed
        _ = typeof(Avalonia.Controls.AutoCompleteBox);
        _ = typeof(Avalonia.Controls.ColorPicker);
        _ = typeof(Avalonia.Controls.DataGrid);
        _ = typeof(Avalonia.Controls.Separator);
        _ = typeof(Avalonia.Controls.Primitives.Popup);
        _ = typeof(Avalonia.Controls.Primitives.TemplatedControl);
        _ = typeof(Avalonia.Controls.Primitives.PopupRoot);
        _ = typeof(Avalonia.Controls.Primitives.AccessText);

        var builder = AppBuilder.Configure<App>()
            .ConfigureFonts(fontManager =>
            {
                fontManager.AddFontCollection(new MyFontCollection());
            })
            .With(new FontManagerOptions
            {
                FontFallbacks = new[]
                {
                    new FontFallback { FontFamily = new Avalonia.Media.FontFamily("avares://AvaloniaHost/Assets/Fonts#Noto Color Emoji") },
                    new FontFallback { FontFamily = new Avalonia.Media.FontFamily("Arial") }
                }
            });
        
        return builder;
    }
}