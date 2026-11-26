// Практика 1, крок 3: гілку перевірки меж перенесено вниз.
int[] scores = [100, 90, 85, 74, 64, 60, 45, 20, -1, 101];
foreach (int score in scores)
{
    string letter = score switch
    {
        >= 90 => "A",
        >= 82 => "B",
        >= 74 => "C",
        >= 64 => "D",
        >= 60 => "E",
        >= 35 => "FX",
        < 0 or > 100 => "помилка",
        _ => "F",
    };
    Console.WriteLine($"{score,4}: {letter}");
}
