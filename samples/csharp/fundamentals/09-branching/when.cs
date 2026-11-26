// when: додаткова умова, яку не можна записати шаблоном (змінна, обчислення).
int limit = 100;
int[] amounts = [-5, 0, 42, 100, 250];
foreach (int amount in amounts)
{
    string verdict = amount switch
    {
        < 0 => "помилка: від'ємна сума",
        0 => "нічого не списано",
        _ when amount > limit => $"перевищено ліміт {limit}",
        var x when x % 2 == 0 => $"парна сума {x}",
        _ => $"сума {amount}",
    };
    Console.WriteLine($"{amount,4}: {verdict}");
}
