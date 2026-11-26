using System.Text;

var sb = new StringBuilder();
sb.AppendLine("n;квадрат");
for (int n = 1; n <= 5; n++)
{
    sb.Append(n).Append(';').Append(n * n).AppendLine();
}
string csv = sb.ToString().TrimEnd();
Console.WriteLine(csv);
Console.WriteLine($"рядків: {csv.Split('\n').Length}");
