// Console.Read повертає код наступного символу з буфера введення або -1, коли введення закінчилося.
int code;
while ((code = Console.Read()) != -1)
{
    string shown = ((char)code).ToString();
    if (code == '\n')
    {
        shown = "\\n";
    }
    if (code == '\r')
    {
        shown = "\\r";
    }
    Console.WriteLine($"{code,5}  {shown}");
}
Console.WriteLine("   -1  кінець введення");
