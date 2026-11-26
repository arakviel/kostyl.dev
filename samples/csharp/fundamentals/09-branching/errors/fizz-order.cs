for (int n = 1; n <= 21; n++)
{
    string text = (n % 2, n % 7) switch
    {
        (0, _) => "Two",
        (0, 0) => "TwoSeven",
        (_, 0) => "Seven",
        _ => n.ToString(),
    };
    Console.Write(text + " ");
}
