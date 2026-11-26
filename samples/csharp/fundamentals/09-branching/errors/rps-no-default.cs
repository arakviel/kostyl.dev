(string, string)[] rounds =
[
    ("камінь", "ножиці"), ("папір", "ножиці"), ("папір", "папір"), ("ножиці", "папір"), ("камінь", "вогонь"),
];
foreach (var (first, second) in rounds)
{
    Console.WriteLine($"{first} проти {second}: {Judge(first, second)}");
}

static string Judge(string a, string b) => (a, b) switch
{
    _ when !IsMove(a) || !IsMove(b) => "невідомий хід",
    _ when a == b => "нічия",
    ("камінь", "ножиці") or ("ножиці", "папір") or ("папір", "камінь") => "виграв перший",
};

static bool IsMove(string s) => s is "камінь" or "ножиці" or "папір";
