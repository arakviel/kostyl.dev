List<int> numbers = [4, -1, 7, -3];
for (int i = numbers.Count - 1; i >= 0; i--)
{
    if (numbers[i] < 0)
        numbers.RemoveAt(i);
}
Console.WriteLine(string.Join(", ", numbers));
