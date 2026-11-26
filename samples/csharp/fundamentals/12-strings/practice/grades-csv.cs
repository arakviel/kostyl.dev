using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

string[] lines =
[
    "Коваль;Олена;10,12,11",
    "Шевчук;Тарас;8,9",
    "Бондар;Ірина;12,10,11,12",
];

Console.WriteLine($"{"Прізвище",-10}{"Ім'я",-8}{"Оцінок",7}{"Середня",9}");
Console.WriteLine(new string('-', 34));
foreach (string line in lines)
{
    string[] fields = line.Split(';');
    string[] marks = fields[2].Split(',');
    int sum = 0;
    foreach (string mark in marks)
        sum += int.Parse(mark);
    double average = (double)sum / marks.Length;
    Console.WriteLine($"{fields[0],-10}{fields[1],-8}{marks.Length,7}{average,9:F2}");
}
