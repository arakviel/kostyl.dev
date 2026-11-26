using System.Text;

// Практика 1: значення чи посилання — передбачте вивід кожного рядка.
int score = 70;
int saved = score;
score += 5;
Console.WriteLine($"1. saved = {saved}");

int[] marks = [5, 4, 3];
int[] backup = marks;
marks[2] = 5;
Console.WriteLine($"2. backup[2] = {backup[2]}");

string city = "Рівне";
string other = city;
other = other.ToUpper();
Console.WriteLine($"3. city = {city}");

StringBuilder report = new("Звіт");
StringBuilder alias = report;
alias.Append(" готовий");
Console.WriteLine($"4. report = {report}");

int[] copy = (int[])marks.Clone();
copy[0] = 1;
Console.WriteLine($"5. marks[0] = {marks[0]}");

object boxed = score;
score = 0;
Console.WriteLine($"6. boxed = {boxed}");
