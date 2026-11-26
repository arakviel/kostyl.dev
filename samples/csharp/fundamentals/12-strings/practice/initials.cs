string[] inputs = ["  олена   петрівна   КОВАЛЬ ", "тарас григорович шевченко", "Ірина Бондар"];
foreach (string input in inputs)
{
    string[] parts = input.Split(' ', StringSplitOptions.RemoveEmptyEntries);
    string surname = Capitalize(parts[^1]);
    string initials = "";
    for (int i = 0; i < parts.Length - 1; i++)
    {
        initials += $" {char.ToUpper(parts[i][0])}.";
    }
    Console.WriteLine($"[{input}] → {surname}{initials}");
}

static string Capitalize(string word) => char.ToUpper(word[0]) + word.Substring(1).ToLower();
