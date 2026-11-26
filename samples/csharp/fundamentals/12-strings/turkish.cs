// Поглиблений розділ: ToUpper і ToLower залежать від культури.
using System.Globalization;

CultureInfo tr = CultureInfo.GetCultureInfo("tr-TR");
CultureInfo uk = CultureInfo.GetCultureInfo("uk-UA");

Console.WriteLine($"\"file\".ToUpper(uk):  {"file".ToUpper(uk)}");
Console.WriteLine($"\"file\".ToUpper(tr):  {"file".ToUpper(tr)}");
Console.WriteLine($"\"FILE\".ToLower(tr):  {"FILE".ToLower(tr)}");
Console.WriteLine($"ToUpperInvariant:    {"file".ToUpperInvariant()}");

CultureInfo.CurrentCulture = tr;
string command = "file";
Console.WriteLine($"tr-TR: command.ToUpper() == \"FILE\": {command.ToUpper() == "FILE"}");
Console.WriteLine($"tr-TR: Equals(\"FILE\", OrdinalIgnoreCase): {command.Equals("FILE", StringComparison.OrdinalIgnoreCase)}");
