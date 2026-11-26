List<string> cities = ["Київ", "Львів", "Одеса"];

foreach (string city in cities)
{
    Console.Write($"{city} ");
}
Console.WriteLine("— foreach");

// те саме вручну: так foreach розгортає компілятор (без try/finally)
var e = cities.GetEnumerator();
while (e.MoveNext())
{
    string city = e.Current;
    Console.Write($"{city} ");
}
Console.WriteLine("— GetEnumerator, MoveNext, Current");
