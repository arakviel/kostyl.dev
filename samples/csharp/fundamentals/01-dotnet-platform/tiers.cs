static int Square(int x) => x * x;

long total = 0;
for (int call = 1; call <= 200; call++)
{
    total += Square(call);
    if (call % 50 == 0) Thread.Sleep(200);
}
Console.WriteLine(total);
