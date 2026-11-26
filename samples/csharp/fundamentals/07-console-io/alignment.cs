using System.Globalization;

// Вирівнювання: {значення,ширина} — праворуч, {значення,-ширина} — ліворуч.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

string[] names = ["Бондар", "Ко", "Шевченко"];
double[] scores = [4.75, 5, 3.5];

Console.WriteLine($"{"Прізвище",-10}|{"Бал",6}|");
for (int i = 0; i < names.Length; i++)
{
    Console.WriteLine($"{names[i],-10}|{scores[i],6:F2}|");
}
Console.WriteLine();
Console.WriteLine($"[{"текст",8}] [{"текст",-8}] [{"довгий текст",8}]");
