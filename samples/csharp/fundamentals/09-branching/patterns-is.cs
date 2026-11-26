// is з шаблонами: константа, відношення, and / or / not, null.
char[] chars = ['q', 'Q', '7', ' ', 'ї'];
foreach (char c in chars)
{
    bool latin = c is >= 'a' and <= 'z' or >= 'A' and <= 'Z';
    bool digit = c is >= '0' and <= '9';
    bool notSpace = c is not ' ';
    Console.WriteLine($"'{c}': латинська {latin,-5}  цифра {digit,-5}  не пробіл {notSpace}");
}
Console.WriteLine();

int code = 404;
Console.WriteLine($"{code} is 404: {code is 404}");
Console.WriteLine($"{code} is >= 400 and < 500: {code is >= 400 and < 500}");
Console.WriteLine($"{code} is 200 or 201 or 204: {code is 200 or 201 or 204}");

string? name = null;
Console.WriteLine($"name is null: {name is null}, name is not null: {name is not null}");
name = "Олена";
Console.WriteLine($"name is null: {name is null}, name is not null: {name is not null}");
