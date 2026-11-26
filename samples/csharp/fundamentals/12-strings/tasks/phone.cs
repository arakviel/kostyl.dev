string[] inputs = ["+38 (050) 123-45-67", "050 123 45 67", "0501234567"];
foreach (string input in inputs)
{
    string digits = input.Replace("+", "").Replace(" ", "").Replace("(", "").Replace(")", "").Replace("-", "");
    if (digits.Length == 10)
        digits = "38" + digits;
    string pretty = $"+{digits.Substring(0, 2)} {digits.Substring(2, 3)} {digits.Substring(5, 3)}-{digits.Substring(8, 2)}-{digits.Substring(10)}";
    Console.WriteLine($"{input,-20} → {pretty}");
}
