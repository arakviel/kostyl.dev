// Змінна присвоюється в обох гілках if, тому читати її після if дозволено.
int score = 75;
string grade;
if (score >= 60)
{
    grade = "зараховано";
}
else
{
    grade = "не зараховано";
}
Console.WriteLine(grade);
