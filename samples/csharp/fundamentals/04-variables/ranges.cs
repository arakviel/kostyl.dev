// Розмір і діапазон цілочисельних типів.
Console.WriteLine("тип     байти               мінімум               максимум");
Console.WriteLine($"sbyte   {sizeof(sbyte),5} {sbyte.MinValue,21} {sbyte.MaxValue,22}");
Console.WriteLine($"byte    {sizeof(byte),5} {byte.MinValue,21} {byte.MaxValue,22}");
Console.WriteLine($"short   {sizeof(short),5} {short.MinValue,21} {short.MaxValue,22}");
Console.WriteLine($"ushort  {sizeof(ushort),5} {ushort.MinValue,21} {ushort.MaxValue,22}");
Console.WriteLine($"int     {sizeof(int),5} {int.MinValue,21} {int.MaxValue,22}");
Console.WriteLine($"uint    {sizeof(uint),5} {uint.MinValue,21} {uint.MaxValue,22}");
Console.WriteLine($"long    {sizeof(long),5} {long.MinValue,21} {long.MaxValue,22}");
Console.WriteLine($"ulong   {sizeof(ulong),5} {ulong.MinValue,21} {ulong.MaxValue,22}");
Console.WriteLine($"nint    {nint.Size,5} {nint.MinValue,21} {nint.MaxValue,22}");
Console.WriteLine($"nuint   {nuint.Size,5} {nuint.MinValue,21} {nuint.MaxValue,22}");
Console.WriteLine();
Console.WriteLine($"Int128 max:  {Int128.MaxValue}");
Console.WriteLine($"UInt128 max: {UInt128.MaxValue}");
