// Анонімні типи: клас без імені, який генерує компілятор.
var student = new { Name = "Олена", Age = 19 };
Console.WriteLine(student);
Console.WriteLine(student.Name);

string city = "Львів";
int year = 2026;
var info = new { city, year };            // імена властивостей беруться з імен змінних
Console.WriteLine(info);

var older = student with { Age = 20 };    // нова копія зі зміненою властивістю
Console.WriteLine($"{student} -> {older}");

var same = new { Name = "Олена", Age = 19 };
Console.WriteLine($"Equals:   {student.Equals(same)}");
Console.WriteLine($"==:       {student == same}");
Console.WriteLine($"один тип: {student.GetType() == same.GetType()}");
Console.WriteLine($"ім'я типу: {student.GetType().Name}");
Console.WriteLine($"значущий: {student.GetType().IsValueType}");
