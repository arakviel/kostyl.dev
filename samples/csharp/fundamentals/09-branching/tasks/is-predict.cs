// Міні-завдання: значення виразів is з логічними шаблонами.
int x = 15;
Console.WriteLine(x is > 10 and < 20);
Console.WriteLine(x is < 10 or > 20);
Console.WriteLine(x is not (> 10 and < 20));
Console.WriteLine(x is 5 or 10 or 15);
Console.WriteLine(x is not 15 and not 16);
char c = 'k';
Console.WriteLine(c is >= 'a' and <= 'f' or >= 'A' and <= 'F' or >= '0' and <= '9');
