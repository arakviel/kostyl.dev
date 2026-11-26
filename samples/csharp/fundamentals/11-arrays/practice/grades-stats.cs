int[] grades = [7, 10, 12, 4, 9, 9, 11, 3, 8, 10, 12, 6, 9, 10, 2, 11, 9, 7, 10, 8];

// індекс масиву — сама оцінка, тому потрібно 13 лічильників: 0..12, нульовий не використовується
int[] counts = new int[13];
foreach (int grade in grades)
{
    counts[grade]++;
}

for (int grade = 12; grade >= 1; grade--)
{
    Console.WriteLine($"{grade,2} | {new string('*', counts[grade])}");
}

// рівні: початковий 1–3, середній 4–6, достатній 7–9, високий 10–12
string[] levels = ["початковий", "середній", "достатній", "високий"];
int[] byLevel = new int[4];
foreach (int grade in grades)
{
    byLevel[(grade - 1) / 3]++;
}
for (int i = 0; i < levels.Length; i++)
{
    Console.WriteLine($"{levels[i]}: {byLevel[i]}");
}
