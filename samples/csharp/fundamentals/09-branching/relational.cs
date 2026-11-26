// Шаблони відношення у switch expression: діапазони температури.
double[] temps = [-12, 0, 7.5, 18, 24.9, 25, 33];
foreach (double t in temps)
{
    string kind = t switch
    {
        < 0 => "мороз",
        < 10 => "холодно",
        >= 10 and < 25 => "тепло",
        >= 25 => "спека",
        _ => "немає даних",
    };
    Console.WriteLine($"{t,6}°: {kind}");
}
Console.WriteLine($"{double.NaN,6}°: {Classify(double.NaN)}");

static string Classify(double t) => t switch
{
    < 0 => "мороз",
    < 10 => "холодно",
    >= 10 and < 25 => "тепло",
    >= 25 => "спека",
    _ => "немає даних",
};
