// Міні-завдання: той самий рядок трьома видами літералів.
string regular = "Файл \"звіт.txt\" лежить у C:\\Docs";
string verbatim = @"Файл ""звіт.txt"" лежить у C:\Docs";
string raw = """Файл "звіт.txt" лежить у C:\Docs""";

Console.WriteLine(regular);
Console.WriteLine(verbatim);
Console.WriteLine(raw);
Console.WriteLine(regular == verbatim && verbatim == raw);
