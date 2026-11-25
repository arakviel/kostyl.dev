Console.WriteLine(Greeting("Олена", 19));

static string Greeting(string name, int age)
{
    string prefix = age >= 18 ? "Вітаю" : "Привіт";
    return prefix + ", " + name + "!";
}
