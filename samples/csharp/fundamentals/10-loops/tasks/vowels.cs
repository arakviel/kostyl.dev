string phrase = "Цикл повторює інструкції";
int vowels = 0;
int consonants = 0;
foreach (char c in phrase)
{
    if ("аеєиіїоуюяАЕЄИІЇОУЮЯ".Contains(c))
        vowels++;
    else if (char.IsLetter(c))
        consonants++;
}
Console.WriteLine($"голосних: {vowels}, приголосних: {consonants}");
