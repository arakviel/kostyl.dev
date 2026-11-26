string[] phrases = ["Я несу гусеня", "Козак з казок!", "Київ — столиця", "А"];
foreach (string phrase in phrases)
{
    Console.WriteLine($"{phrase,-16} → {IsPalindrome(phrase)}");
}

static bool IsPalindrome(string text)
{
    int left = 0;
    int right = text.Length - 1;
    while (left < right)
    {
        if (!char.IsLetter(text[left]))
        {
            left++;
            continue;
        }
        if (!char.IsLetter(text[right]))
        {
            right--;
            continue;
        }
        if (char.ToLowerInvariant(text[left]) != char.ToLowerInvariant(text[right]))
            return false;
        left++;
        right--;
    }
    return true;
}
