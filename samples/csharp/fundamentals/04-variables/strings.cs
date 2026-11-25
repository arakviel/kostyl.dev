// Три види рядкових літералів і інтерполяція.
string path1 = "C:\\Users\\student\\notes.txt";
string path2 = @"C:\Users\student\notes.txt";
string path3 = """C:\Users\student\notes.txt""";
Console.WriteLine(path1);
Console.WriteLine(path1 == path2 && path2 == path3);

string quote = @"Він сказав: ""Привіт""";
Console.WriteLine(quote);

string json = """
    {
      "name": "Олена",
      "age": 19
    }
    """;
Console.WriteLine(json);

string name = "Олена";
int age = 19;
Console.WriteLine($"{name}: {age} років, через рік буде {age + 1}");
