string settings = "name = Олена; age=19 ;city=Львів;;";

string[] pairs = settings.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
foreach (string pair in pairs)
{
    string[] kv = pair.Split('=', StringSplitOptions.TrimEntries);
    Console.WriteLine($"{kv[0],-5} → {kv[1]}");
}
