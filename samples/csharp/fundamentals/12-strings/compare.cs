string a = "Київ";
string b = "КИЇВ";

Console.WriteLine($"a == b:                             {a == b}");
Console.WriteLine($"a.Equals(b, OrdinalIgnoreCase):     {a.Equals(b, StringComparison.OrdinalIgnoreCase)}");
Console.WriteLine($"string.Equals(a, b, CurrentCultureIgnoreCase): {string.Equals(a, b, StringComparison.CurrentCultureIgnoreCase)}");

// порядок: від'ємне — a раніше, 0 — рівні, додатне — a пізніше
Console.WriteLine($"Compare(\"груша\", \"яблуко\", Ordinal):   {string.Compare("груша", "яблуко", StringComparison.Ordinal)}");
Console.WriteLine($"Compare(\"яблуко\", \"їжак\", Ordinal):    {string.Compare("яблуко", "їжак", StringComparison.Ordinal)}");
Console.WriteLine($"Compare(\"a\", \"B\", Ordinal):            {string.Compare("a", "B", StringComparison.Ordinal)}");
Console.WriteLine($"Compare(\"a\", \"B\", InvariantCulture):   {string.Compare("a", "B", StringComparison.InvariantCulture)}");

// пошук з урахуванням регістру і без
string command = "Save File";
Console.WriteLine($"Contains(\"file\"):                     {command.Contains("file")}");
Console.WriteLine($"Contains(\"file\", OrdinalIgnoreCase):  {command.Contains("file", StringComparison.OrdinalIgnoreCase)}");
Console.WriteLine($"StartsWith(\"save\", OrdinalIgnoreCase): {command.StartsWith("save", StringComparison.OrdinalIgnoreCase)}");
