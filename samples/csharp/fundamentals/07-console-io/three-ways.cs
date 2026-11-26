using System.Globalization;

// Три способи зібрати рядок для виводу: склеювання, складене форматування, інтерполяція.
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");   // вивід як на українській Windows

string name = "Олена";
int age = 19;
double average = 4.567;

Console.WriteLine("Студентка " + name + ", вік " + age + ", середній бал " + average);
Console.WriteLine("Студентка {0}, вік {1}, середній бал {2:F1}", name, age, average);
string text = string.Format("Студентка {0}, вік {1}", name, age);
Console.WriteLine(text);
Console.WriteLine($"Студентка {name}, вік {age}, середній бал {average:F1}");
