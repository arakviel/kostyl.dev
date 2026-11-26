using System.Globalization;

// Міні-завдання: введення оцінки 1–12 (дробової) до коректного значення; культура uk-UA — роздільник кома.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

double grade;
while (true)
{
    Console.Write("Оцінка (1–12): ");
    string? input = Console.ReadLine();
    if (input is null)
    {
        return;
    }
    if (double.TryParse(input, out grade) && grade >= 1 && grade <= 12)
    {
        break;
    }
    Console.WriteLine($"\"{input}\" — не оцінка від 1 до 12");
}
Console.WriteLine($"Прийнято: {grade:F1}");
