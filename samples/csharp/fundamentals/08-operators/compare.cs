// Оператори порівняння: результат завжди bool.
int a = 3, b = 5;
Console.WriteLine($"a == b: {a == b}");
Console.WriteLine($"a != b: {a != b}");
Console.WriteLine($"a <  b: {a < b}");
Console.WriteLine($"a >  b: {a > b}");
Console.WriteLine($"a <= 3: {a <= 3}");
Console.WriteLine($"a >= 4: {a >= 4}");
Console.WriteLine();

bool less = a < b;   // результат порівняння можна зберегти в змінну
Console.WriteLine($"less = {less}");

char c = 'k';
Console.WriteLine($"'k' < 'z': {c < 'z'} (коди {(int)c} і {(int)'z'})");

string s1 = "кіт";
string s2 = "кі" + "т";
Console.WriteLine($"s1 == s2: {s1 == s2}");

double sum = 0.1 + 0.2;
Console.WriteLine($"0.1 + 0.2 == 0.3: {sum == 0.3}");
