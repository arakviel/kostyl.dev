using System.Globalization;

// Міні-завдання: той самий рядок трьома способами.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
string city = "Житомир";
int population = 261624;
double area = 65;
double density = population / area;

Console.WriteLine(city + ": " + population + " мешканців, " + area + " км², густота " + density.ToString("F1") + " осіб/км²");
Console.WriteLine("{0}: {1} мешканців, {2} км², густота {3:F1} осіб/км²", city, population, area, density);
Console.WriteLine($"{city}: {population} мешканців, {area} км², густота {density:F1} осіб/км²");
