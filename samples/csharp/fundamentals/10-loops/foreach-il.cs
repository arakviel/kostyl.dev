// Поглиблений розділ: дивитися IL через ilspycmd -il на Release-збірці.
int[] numbers = [1, 2, 3];
List<int> list = [1, 2, 3];
Console.WriteLine(SumArray(numbers));
Console.WriteLine(CountSpaces("a b c"));
Console.WriteLine(SumList(list));

static int SumArray(int[] items)
{
    int sum = 0;
    foreach (int item in items)
        sum += item;
    return sum;
}

static int CountSpaces(string text)
{
    int count = 0;
    foreach (char c in text)
        if (c == ' ')
            count++;
    return count;
}

static int SumList(List<int> items)
{
    int sum = 0;
    foreach (int item in items)
        sum += item;
    return sum;
}
