using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

decimal amount = 10_000m;
decimal rate = 0m;        // ставка 0 %: без запобіжника цикл не завершиться
int years = 0;
while (amount < 20_000m && years < 100)
{
    amount += amount * rate;
    years++;
}
if (amount >= 20_000m)
    Console.WriteLine($"сума подвоїлася за {years} р.");
else
    Console.WriteLine($"за {years} р. сума не подвоїлася: {amount:F2} грн");
