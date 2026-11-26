// Звернення до члена через null: попередження CS8602 під час компіляції і виняток під час роботи.
string? name = null;
Console.WriteLine("до звернення");
Console.WriteLine(name.Length);
Console.WriteLine("після звернення");
