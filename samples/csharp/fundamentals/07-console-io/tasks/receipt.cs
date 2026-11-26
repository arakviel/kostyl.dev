using System.Globalization;

// Міні-завдання: таблиця покупок з вирівнюванням.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

string[] items = ["Хліб", "Молоко 2,5%", "Сир"];
int[] quantities = [2, 1, 3];
decimal[] prices = [28.50m, 42.90m, 115m];

Console.WriteLine($"{"Товар",-14}{"К-сть",6}{"Ціна",10}{"Сума",10}");
decimal total = 0;
for (int i = 0; i < items.Length; i++)
{
    decimal sum = quantities[i] * prices[i];
    total += sum;
    Console.WriteLine($"{items[i],-14}{quantities[i],6}{prices[i],10:F2}{sum,10:F2}");
}
Console.WriteLine($"{"Разом",-30}{total,10:F2}");
