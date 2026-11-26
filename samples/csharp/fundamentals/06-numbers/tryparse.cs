// Які рядки int.TryParse вважає числом.
string?[] inputs = ["42", " 42 ", "+42", "-0", "4 2", "42.0", "1_000", "", "3000000000", null];
Console.WriteLine("рядок          успіх  результат");
foreach (string? s in inputs)
{
    bool ok = int.TryParse(s, out int n);
    Console.WriteLine($"{Show(s),-14} {ok,-6} {n}");
}

static string Show(string? s) => s is null ? "null" : $"\"{s}\"";
