using System.Globalization;

// Практика 1: чек магазину з датою, вирівнюванням і грошовим форматом.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
DateTime when = new DateTime(2026, 11, 25, 18, 42, 0);

string[] items = ["Зошит 48 арк.", "Ручка", "Олівець HB"];
int[] quantities = [3, 2, 5];
decimal[] prices = [24.90m, 18.00m, 7.50m];

Console.WriteLine($"{"КАНЦТОВАРИ",25}");
Console.WriteLine($"Чек від {when:dd.MM.yyyy HH:mm}");
Console.WriteLine(new string('-', 40));
decimal total = 0;
for (int i = 0; i < items.Length; i++)
{
    decimal sum = quantities[i] * prices[i];
    total += sum;
    Console.WriteLine($"{items[i],-16}{quantities[i],3} x {prices[i],7:F2}{sum,11:F2}");
}
Console.WriteLine(new string('-', 40));
Console.WriteLine($"{"До сплати:",-29}{total,11:C}");
