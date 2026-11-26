using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

// м'який перенос U+00AD: невидимий символ, який часто приходить разом з текстом, скопійованим із сайту
string pasted = "інфор\u00ADмація";
string word = "інформація";

Console.WriteLine($"Length: {pasted.Length} і {word.Length}");
Console.WriteLine($"pasted == word:                   {pasted == word}");
Console.WriteLine($"Contains(word):                   {pasted.Contains(word)}");
Console.WriteLine($"IndexOf(word):                    {pasted.IndexOf(word)}");
Console.WriteLine($"IndexOf(word, Ordinal):           {pasted.IndexOf(word, StringComparison.Ordinal)}");
Console.WriteLine($"StartsWith(word):                 {pasted.StartsWith(word)}");
Console.WriteLine($"StartsWith(word, Ordinal):        {pasted.StartsWith(word, StringComparison.Ordinal)}");
Console.WriteLine($"string.Compare(pasted, word):     {string.Compare(pasted, word)}");
