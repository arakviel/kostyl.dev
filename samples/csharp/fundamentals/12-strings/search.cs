string text = "мама мила раму, а Марко мив вікно";

Console.WriteLine($"IndexOf('м'):         {text.IndexOf('м')}");
Console.WriteLine($"IndexOf('м', 1):      {text.IndexOf('м', 1)}");
Console.WriteLine($"IndexOf(\"ми\"):        {text.IndexOf("ми")}");
Console.WriteLine($"LastIndexOf('м'):     {text.LastIndexOf('м')}");
Console.WriteLine($"IndexOf('ж'):         {text.IndexOf('ж')}");
Console.WriteLine($"IndexOfAny([',', '.']): {text.IndexOfAny([',', '.'])}");
Console.WriteLine($"Contains(\"раму\"):     {text.Contains("раму")}");
Console.WriteLine($"StartsWith(\"мама\"):   {text.StartsWith("мама")}");
Console.WriteLine($"EndsWith(\"вікно\"):    {text.EndsWith("вікно")}");
Console.WriteLine($"Contains(\"марко\"):    {text.Contains("марко")}");

// усі входження: пошук з позиції після попереднього
Console.Write("усі 'м':");
int pos = text.IndexOf('м');
while (pos != -1)
{
    Console.Write($" {pos}");
    pos = text.IndexOf('м', pos + 1);
}
Console.WriteLine();

string? nothing = null;
Console.WriteLine($"IsNullOrEmpty(null): {string.IsNullOrEmpty(nothing)}, IsNullOrWhiteSpace(\"  \"): {string.IsNullOrWhiteSpace("  ")}");
