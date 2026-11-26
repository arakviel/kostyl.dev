// Міні-завдання: FizzBuzz з дільниками 2 і 7.
for (int n = 1; n <= 21; n++)
{
    string text = (n % 2, n % 7) switch
    {
        (0, 0) => "TwoSeven",
        (0, _) => "Two",
        (_, 0) => "Seven",
        _ => n.ToString(),
    };
    Console.Write(text + " ");
}
Console.WriteLine();
