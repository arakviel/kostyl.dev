// Програма-«ліцензія»: на ній лекція показує декомпіляцію та обфускацію.
// Ключ зашито в код, і саме це робить програму вразливою.
Console.Write("Ключ ліцензії: ");
string? key = Console.ReadLine();

if (IsValidKey(key))
{
    Console.WriteLine("Ліцензію активовано.");
}
else
{
    Console.WriteLine("Невірний ключ.");
}

static bool IsValidKey(string? key)
{
    string secret = "KOSTYL-2026-PRO";
    return key == secret;
}
