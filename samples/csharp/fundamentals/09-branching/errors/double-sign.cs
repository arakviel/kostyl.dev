double v = 0.5;
string sign = v switch
{
    < 0 => "від'ємне",
    0 => "нуль",
    > 0 => "додатне",
};
Console.WriteLine(sign);
