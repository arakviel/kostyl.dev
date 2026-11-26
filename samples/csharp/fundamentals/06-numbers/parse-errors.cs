// Parse кидає виняток для рядка, який не є числом потрібного типу.
// Запуск: dotnet run parse-errors.cs -- <рядок>
string input = args.Length > 0 ? args[0] : "abc";
Console.WriteLine($"int.Parse(\"{input}\")...");
int value = int.Parse(input);
Console.WriteLine(value);
