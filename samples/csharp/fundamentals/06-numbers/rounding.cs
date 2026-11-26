// Приведення відкидає дробову частину, Math.Round округлює до парного, Floor/Ceiling — вниз/вгору.
double[] values = [2.4, 2.5, 2.6, 3.5, -2.5, -2.7];
Console.WriteLine("    x  (int)x  Round  AwayFromZero  Floor  Ceiling  Convert.ToInt32");
foreach (double x in values)
{
    Console.WriteLine($"{x,5}  {(int)x,6}  {Math.Round(x),5}  {Math.Round(x, MidpointRounding.AwayFromZero),12}  " +
                      $"{Math.Floor(x),5}  {Math.Ceiling(x),7}  {Convert.ToInt32(x),15}");
}
Console.WriteLine();
Console.WriteLine($"Math.Round(2.665m, 2)               = {Math.Round(2.665m, 2)}");
Console.WriteLine($"Math.Round(2.665m, 2, AwayFromZero) = {Math.Round(2.665m, 2, MidpointRounding.AwayFromZero)}");
