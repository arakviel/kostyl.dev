// UTF-8 літерали (u8) і raw-рядки з інтерполяцією, де фігурні дужки — звичайний текст.
string text = "Привіт";
ReadOnlySpan<byte> bytes = "Привіт"u8;
Console.WriteLine($"символів UTF-16: {text.Length}, байтів UTF-8: {bytes.Length}");

string name = "Олена";
string json = $$"""
    {
      "name": "{{name}}",
      "tags": {}
    }
    """;
Console.WriteLine(json);
