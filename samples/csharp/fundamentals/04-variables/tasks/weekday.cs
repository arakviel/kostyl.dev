// Міні-завдання: виправлена версія — kind присвоюється на кожному шляху.
int day = 6;
string kind;
if (day <= 5)
{
    kind = "робочий";
}
else
{
    kind = "вихідний";
}
Console.WriteLine($"День {day}: {kind}");
