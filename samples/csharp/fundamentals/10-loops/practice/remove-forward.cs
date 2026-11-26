List<int> numbers = [3, -1, -2, 4, -5];
for (int i = 0; i < numbers.Count; i++)
{
    if (numbers[i] < 0)
        numbers.RemoveAt(i);
}
Console.WriteLine(string.Join(", ", numbers));
