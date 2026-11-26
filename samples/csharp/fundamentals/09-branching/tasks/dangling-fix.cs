// Міні-завдання: фігурні дужки прив'язують else до зовнішнього if.
(int a, int b)[] pairs = [(5, -1), (5, 3), (-2, -1)];
foreach (var (a, b) in pairs)
{
    string message = "нічого не надруковано";
    if (a > 0)
    {
        if (b > 0)
            message = "обидва додатні";
    }
    else
        message = "a не додатне";
    Console.WriteLine($"a = {a,2}, b = {b,2}: {message}");
}
