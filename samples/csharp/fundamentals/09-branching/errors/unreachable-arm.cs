int t = 20;
string kind = t switch
{
    _ => "невідомо",
    < 0 => "мороз",
};
Console.WriteLine(kind);
