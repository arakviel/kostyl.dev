int[] samples = [90210, 7, 0];
foreach (int sample in samples)
{
    int n = sample;
    int byWhile = 0;
    while (n > 0)
    {
        n /= 10;
        byWhile++;
    }

    n = sample;
    int byDoWhile = 0;
    do
    {
        n /= 10;
        byDoWhile++;
    } while (n > 0);

    Console.WriteLine($"{sample,6}: while — {byWhile}, do-while — {byDoWhile}");
}
