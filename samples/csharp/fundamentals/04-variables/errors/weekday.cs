int day = 6;
string kind;
if (day <= 5)
{
    kind = "робочий";
}
else if (day == 6 || day == 7)
{
    kind = "вихідний";
}
Console.WriteLine(kind);
