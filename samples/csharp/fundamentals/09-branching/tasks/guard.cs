// Міні-завдання: перевірка введення через guard clause.
string[] inputs = ["17", "abc", "-3", "130", "45"];
foreach (string input in inputs)
{
    Console.WriteLine($"{input,4}: {Check(input)}");
}

static string Check(string text)
{
    if (!int.TryParse(text, out int age))
        return "не число";
    if (age < 0 || age > 120)
        return "неможливий вік";
    if (age < 18)
        return $"неповнолітній, до 18 лишилось {18 - age}";
    return $"повнолітній, {age} років";
}
