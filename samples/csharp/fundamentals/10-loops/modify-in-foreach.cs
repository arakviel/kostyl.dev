List<int> numbers = [4, -1, 7, -3];
foreach (int n in numbers)
{
    if (n < 0)
        numbers.Remove(n);   // зміна списку під час перебору
}
Console.WriteLine(string.Join(", ", numbers));
