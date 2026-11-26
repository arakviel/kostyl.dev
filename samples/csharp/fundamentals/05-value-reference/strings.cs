// string — посилальний незмінний тип.
string s1 = "Привіт";
string s2 = s1;
s2 += "!";
Console.WriteLine($"s1 = {s1}, s2 = {s2}");

string upper = s1.ToUpper();
Console.WriteLine($"s1 = {s1}, upper = {upper}");

string a = "Hi";
string b = "Hi";
string c = "H";
c += "i";
Console.WriteLine($"a == c                      {a == c}");
Console.WriteLine($"ReferenceEquals(a, b)       {object.ReferenceEquals(a, b)}");
Console.WriteLine($"ReferenceEquals(a, c)       {object.ReferenceEquals(a, c)}");
Console.WriteLine($"ReferenceEquals(a, Intern)  {object.ReferenceEquals(a, string.Intern(c))}");
