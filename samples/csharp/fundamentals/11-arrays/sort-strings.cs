using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

string[] words = ["яблуко", "їжак", "груша", "ґанок", "єнот", "іній", "абрикос"];

string[] byCulture = (string[])words.Clone();
Array.Sort(byCulture);
Console.WriteLine($"за культурою uk-UA: {string.Join(", ", byCulture)}");

string[] byCode = (string[])words.Clone();
Array.Sort(byCode, StringComparer.Ordinal);
Console.WriteLine($"за кодами символів: {string.Join(", ", byCode)}");
