using System.Text;

var sb = new StringBuilder();
sb.Append("Звіт");
sb.Append(' ');
sb.Append(2026);
sb.AppendLine();
sb.AppendLine("рядок 1");
sb.Append($"рядок {1 + 1}");
Console.WriteLine(sb.ToString());
Console.WriteLine($"Length: {sb.Length}");

sb.Clear();
sb.Append("кіт");
sb.Insert(0, "сірий ");
sb.Replace("кіт", "пес");
sb[0] = 'С';                  // StringBuilder можна змінювати за індексом
Console.WriteLine(sb);

// кома між елементами: прибрати останню після циклу
int[] scores = [90, 75, 60];
var csv = new StringBuilder();
foreach (int s in scores)
{
    csv.Append(s).Append(',');
}
csv.Length--;                 // відкинути останній символ
Console.WriteLine(csv);
