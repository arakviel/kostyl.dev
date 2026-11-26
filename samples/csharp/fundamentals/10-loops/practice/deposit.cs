using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

decimal amount = 10_000m;
decimal rate = 0.12m;     // 12 % на рік
int years = 0;
while (amount < 20_000m)
{
    amount += amount * rate;
    years++;
    Console.WriteLine($"рік {years}: {amount:F2} грн");
}
Console.WriteLine($"сума подвоїлася за {years} р.");
