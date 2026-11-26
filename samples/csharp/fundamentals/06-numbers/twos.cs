// Доповняльний код: як записано від'ємні числа. Формат B8 / B32 друкує біти (з .NET 8).
sbyte[] values = [0, 1, 127, -1, -2, -128];
foreach (sbyte v in values)
{
    Console.WriteLine($"{v,5}  {v:B8}  ті самі біти як byte: {(byte)v,3}");
}
Console.WriteLine();
Console.WriteLine($"int -1:           {-1:B32}");
Console.WriteLine($"int.MinValue:     {int.MinValue:B32}");
Console.WriteLine($"int.MaxValue:     {int.MaxValue:B32}");
