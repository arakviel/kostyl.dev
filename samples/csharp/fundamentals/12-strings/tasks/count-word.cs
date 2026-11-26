string text = "Мама мила раму, а мама Марка мила вікно";
string target = "ма";

int count = 0;
int pos = text.IndexOf(target, StringComparison.Ordinal);
while (pos != -1)
{
    count++;
    pos = text.IndexOf(target, pos + target.Length, StringComparison.Ordinal);
}
Console.WriteLine($"\"{target}\" з урахуванням регістру: {count}");

count = 0;
pos = text.IndexOf(target, StringComparison.OrdinalIgnoreCase);
while (pos != -1)
{
    count++;
    pos = text.IndexOf(target, pos + target.Length, StringComparison.OrdinalIgnoreCase);
}
Console.WriteLine($"\"{target}\" без урахування регістру: {count}");
