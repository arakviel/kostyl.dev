// Значення за замовчуванням: усі біти нульові.
Console.WriteLine(default(int));
Console.WriteLine(default(double));
Console.WriteLine(default(bool));
Console.WriteLine((int)default(char));

int counter = default;   // тип береться з лівої частини
string? text = default;
Console.WriteLine(counter);
Console.WriteLine(text == null);
