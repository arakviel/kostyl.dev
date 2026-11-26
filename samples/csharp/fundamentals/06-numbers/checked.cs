// checked перетворює тихе переповнення на виняток OverflowException.
int max = int.MaxValue;

int wrapped = unchecked(max + 1);
Console.WriteLine($"unchecked(max + 1) = {wrapped}");

long total;
checked
{
    int a = 2_000_000_000, c = 2_000_000_000;
    Console.WriteLine("рахуємо a + c у блоці checked...");
    total = a + c;
}
Console.WriteLine(total);
