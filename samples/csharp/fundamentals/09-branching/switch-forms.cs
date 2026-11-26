// Будова switch statement: одна мітка, кілька міток, блок у секції, goto case, default, return.
int[] codes = [1, 2, 3, 4, 5, 9];
foreach (int code in codes)
{
    Console.Write($"{code}: ");
    switch (code)
    {
        case 1:
            Console.WriteLine("один");
            break;
        case 2:
        case 3:
            Console.WriteLine("два або три");
            break;
        case 4:
        {
            int square = code * code;
            Console.WriteLine($"чотири, квадрат {square}");
            break;
        }
        case 5:
            Console.Write("п'ять -> ");
            goto case 1;
        default:
            Console.WriteLine("інше");
            break;
    }
}
Console.WriteLine(DayName(3));

static string DayName(int day)
{
    switch (day)
    {
        case 1: return "понеділок";
        case 2: return "вівторок";
        case 3: return "середа";
        default: return "інший день";
    }
}
