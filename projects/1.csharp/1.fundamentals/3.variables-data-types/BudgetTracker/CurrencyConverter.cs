namespace BudgetTracker;

public class CurrencyConverter
{
    private static readonly decimal UahToUsd = 0.027m;
    private static readonly decimal UahToEur = 0.025m;
    private static readonly decimal UsdToUah = 37.00m;
    private static readonly decimal EurToUah = 40.50m;

    public static decimal ConvertToUsd(decimal amountInUah)
    {
        return amountInUah * UahToUsd;
    }

    public static decimal ConvertToEur(decimal amountInUah)
    {
        return amountInUah * UahToEur;
    }

    public static decimal ConvertFromUsd(decimal amountInUsd)
    {
        return amountInUsd * UsdToUah;
    }

    public static decimal ConvertFromEur(decimal amountInEur)
    {
        return amountInEur * EurToUah;
    }

    public static void DisplayConversions(decimal amountInUah)
    {
        decimal usd = ConvertToUsd(amountInUah);
        decimal eur = ConvertToEur(amountInUah);

        Console.WriteLine($"\n{amountInUah:F2} UAH =");
        Console.WriteLine($"  {usd:F2} USD");
        Console.WriteLine($"  {eur:F2} EUR");
    }
}
