using System.Globalization;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

string[] students = ["Олена", "Тарас", "Ірина"];
int[][] marks = [[10, 12, 11], [8, 9], [12, 10, 11, 12]];

for (int i = 0; i < students.Length; i++)
{
    int sum = 0;
    foreach (int mark in marks[i])
        sum += mark;
    Console.WriteLine($"{students[i]}: оцінок {marks[i].Length}, середня {(double)sum / marks[i].Length:F1}");
}
