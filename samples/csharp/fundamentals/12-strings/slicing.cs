string date = "2026-11-26";
Console.WriteLine($"Substring(0, 4): {date.Substring(0, 4)}");
Console.WriteLine($"Substring(5, 2): {date.Substring(5, 2)}");
Console.WriteLine($"Substring(8):    {date.Substring(8)}");

string[] pieces = date.Split('-');
Console.WriteLine($"Split('-'): {pieces.Length} частини: {string.Join(" / ", pieces)}");

string messy = " Київ, Львів ,,Одеса ";
string[] raw = messy.Split(',');
Console.WriteLine($"Split(','): {raw.Length}: [{string.Join("][", raw)}]");
string[] clean = messy.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
Console.WriteLine($"з опціями:  {clean.Length}: [{string.Join("][", clean)}]");

string sentence = "один два  три";
string[] words = sentence.Split([' '], StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"слів: {words.Length}");

string padded = "   **Київ**   ";
Console.WriteLine($"Trim():          [{padded.Trim()}]");
Console.WriteLine($"TrimStart():     [{padded.TrimStart()}]");
Console.WriteLine($"Trim(' ', '*'):  [{padded.Trim(' ', '*')}]");
