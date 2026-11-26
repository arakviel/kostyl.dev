// Фігурні дужки як текст і умовний вираз в інтерполяції.
int age = 17;
Console.WriteLine($"{{age}} = {age}");
Console.WriteLine($"Повнолітній: {(age >= 18 ? "так" : "ні")}");
Console.WriteLine("{0} у фігурних дужках: {{{0}}}", age);
