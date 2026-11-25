using System.Text;

// Шукає у будь-якому файлі рядок у кодуванні UTF-16 (так .NET зберігає рядкові літерали)
// і друкує 20 символів, що починаються з нього. Використання:
//   dotnet run find-utf16.cs -- <файл> <початок рядка>
if (args.Length != 2)
{
    Console.WriteLine("Використання: dotnet run find-utf16.cs -- <файл> <текст>");
    return 1;
}

byte[] data = File.ReadAllBytes(args[0]);
byte[] pattern = Encoding.Unicode.GetBytes(args[1]);
int found = 0;

for (int i = 0; i <= data.Length - pattern.Length; i++)
{
    if (data.AsSpan(i, pattern.Length).SequenceEqual(pattern))
    {
        var text = new StringBuilder();
        for (int c = 0; c < 20 && i + 2 * c + 1 < data.Length; c++)
        {
            char ch = (char)(data[i + 2 * c] | data[i + 2 * c + 1] << 8);
            bool readable = ch is (>= ' ' and <= '~') or (>= 'А' and <= 'ї');
            text.Append(readable ? ch : '.');
        }
        Console.WriteLine($"зсув {i,9}: {text}");
        found++;
    }
}

Console.WriteLine($"Знайдено: {found}");
return 0;
