// Як форматування округлює половину: стандартні й власні формати, double і decimal (InvariantCulture).
using System.Globalization;
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
double[] xs = [0.5, 1.5, 2.5, 3.5, -2.5, 1.25, 1.35, 7.25, -7.25, 0.125, 2.675];
foreach (double x in xs)
    Console.WriteLine($"{x,6}  F0={x:F0}  0={x:0}  F1={x:F1}  0.0={x:0.0}  F2={x:F2}  0.00={x:0.00}");
decimal[] ms = [2.5m, 3.5m, 1.25m, 7.25m, 2.675m];
foreach (decimal m in ms)
    Console.WriteLine($"{m,6}m F0={m:F0}  0={m:0}  F1={m:F1}  0.0={m:0.0}  F2={m:F2}");
