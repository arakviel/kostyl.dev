// Практика 2: виправлена версія practice/errors/broken.cs.
int total = 0;
int bonus = 300;
float rate = 0.15f;
var name = "Олена";
const int Limit = 10;
if (total > Limit)
{
    int extra = 5;
    Console.WriteLine(extra);
}
Console.WriteLine($"{total} {bonus} {rate} {name} {Limit}");
