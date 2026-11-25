Console.WriteLine($"int    -> {typeof(int).FullName}, {sizeof(int)} байти");
Console.WriteLine($"long   -> {typeof(long).FullName}, {sizeof(long)} байтів");
Console.WriteLine($"double -> {typeof(double).FullName}, {sizeof(double)} байтів");
Console.WriteLine($"char   -> {typeof(char).FullName}, {sizeof(char)} байти");
Console.WriteLine($"bool   -> {typeof(bool).FullName}, {sizeof(bool)} байт");
Console.WriteLine($"string -> {typeof(string).FullName}");

int a = 42;
System.Int32 b = 42;
Console.WriteLine($"int і System.Int32 — один тип: {a.GetType() == b.GetType()}");
