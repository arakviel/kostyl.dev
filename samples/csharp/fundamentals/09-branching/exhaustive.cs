// Повнота: для int шаблони < 0, 0, > 0 покривають усі значення — попередження немає.
int[] values = [-3, 0, 8];
foreach (int v in values)
{
    string sign = v switch
    {
        < 0 => "від'ємне",
        0 => "нуль",
        > 0 => "додатне",
    };
    Console.WriteLine($"{v}: {sign}");
}

bool ready = true;
string state = ready switch
{
    true => "готово",
    false => "ще ні",
};
Console.WriteLine(state);
