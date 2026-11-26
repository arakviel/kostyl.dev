// Аналіз null: перевірка, атрибут NotNullWhen у string.IsNullOrWhiteSpace і оператор !.
string? input = Console.ReadLine();

if (!string.IsNullOrWhiteSpace(input))
{
    Console.WriteLine(input.Trim());   // без попередження: компілятор знає, що input не null
}

string? maybe = null;
string sure = maybe!;                  // ! вимикає попередження, але null лишається
Console.WriteLine(sure is null);

Console.WriteLine(Describe("Олена"));
Console.WriteLine(Describe(null));

static string Describe(string? name) => name ?? "(немає імені)";
