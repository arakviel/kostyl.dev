using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;

namespace AvaloniaHost.ViewModels;

public partial class MainViewModel : ViewModelBase
{
    public static MainViewModel Instance { get; private set; } = null!;

    public MainViewModel()
    {
        Instance = this;
    }

    [ObservableProperty]
    private string _greeting = "Welcome to Avalonia!";

    [ObservableProperty]
    private int _counter = 0;

    public Action<string>? OnMessageAction { get; set; }

    [RelayCommand]
    private void IncrementCounter()
    {
        Counter++;
    }

    [RelayCommand]
    private void ShowMessage(string message)
    {
        OnMessageAction?.Invoke(message);
    }
}
