// if / else if / else, guard clause з TryParse і область видимості out-змінної.
int[] scores = [95, 74, 60, 12];
foreach (int score in scores)
{
    string grade;
    if (score >= 90)
        grade = "відмінно";
    else if (score >= 75)
        grade = "добре";
    else if (score >= 60)
        grade = "задовільно";
    else
        grade = "незадовільно";
    Console.WriteLine($"{score,3}: {grade}");
}
Console.WriteLine();

string[] inputs = ["42", "abc", "-5"];
foreach (string input in inputs)
{
    Console.WriteLine($"{input}: {Describe(input)}");
}

static string Describe(string text)
{
    if (!int.TryParse(text, out int value))
        return "не число";
    if (value < 0)
        return "від'ємне число";
    // value оголошено в умові першого if, але воно видиме й тут
    return $"число {value}, квадрат {value * value}";
}
