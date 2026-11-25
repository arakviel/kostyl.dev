// Цілі літерали: системи числення, роздільник _, тип без суфікса і з суфіксами.
int dec = 255;
int hex = 0xFF;
int bin = 0b1111_1111;
int million = 1_000_000;
int notOctal = 010;
Console.WriteLine($"{dec} {hex} {bin} {million} {notOctal}");
Console.WriteLine();

Console.WriteLine($"2_147_483_647             {(2_147_483_647).GetType()}");
Console.WriteLine($"2_147_483_648             {(2_147_483_648).GetType()}");
Console.WriteLine($"4_294_967_296             {(4_294_967_296).GetType()}");
Console.WriteLine($"9_223_372_036_854_775_808 {(9_223_372_036_854_775_808).GetType()}");
Console.WriteLine();

Console.WriteLine($"5U   {5U.GetType()}");
Console.WriteLine($"5L   {5L.GetType()}");
Console.WriteLine($"5UL  {5UL.GetType()}");
Console.WriteLine($"5f   {5f.GetType()}");
Console.WriteLine($"5d   {5d.GetType()}");
Console.WriteLine($"5m   {5m.GetType()}");
Console.WriteLine($"5e3  {5e3.GetType()} {5e3}");
