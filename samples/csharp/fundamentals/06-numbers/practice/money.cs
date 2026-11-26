// Практика 3: копійки в double і decimal, банківське і «шкільне» округлення.
double sumD = 0;
decimal sumM = 0;
for (int k = 0; k < 10; k++)
{
    sumD += 0.10;
    sumM += 0.10m;
}
Console.WriteLine($"10 × 0.10 у double:  {sumD}");
Console.WriteLine($"10 × 0.10 у decimal: {sumM}");
Console.WriteLine();

decimal[] amounts = [12.345m, 12.355m, 0.125m, 0.135m, 7.005m, 7.015m];
decimal sumExact = 0, sumEven = 0, sumAway = 0;
Console.WriteLine("сума      ToEven  AwayFromZero");
foreach (decimal x in amounts)
{
    decimal even = Math.Round(x, 2);
    decimal away = Math.Round(x, 2, MidpointRounding.AwayFromZero);
    sumExact += x;
    sumEven += even;
    sumAway += away;
    Console.WriteLine($"{x,7}  {even,6}  {away,12}");
}
Console.WriteLine($"разом: {sumExact}  {sumEven,6}  {sumAway,12}");
