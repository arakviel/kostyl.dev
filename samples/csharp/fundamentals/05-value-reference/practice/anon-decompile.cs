// Практика 3: анонімний тип у декомпіляторі.
var phone = new { Model = "Pixel", Storage = 128 };
var same = new { Model = "Pixel", Storage = 128 };
var other = new { Storage = 128, Model = "Pixel" };

Console.WriteLine(phone);
Console.WriteLine($"phone.Equals(same): {phone.Equals(same)}");
Console.WriteLine($"phone == same: {phone == same}");
Console.WriteLine($"той самий тип, що й other: {phone.GetType() == other.GetType()}");
Console.WriteLine(phone.GetType().Name);
Console.WriteLine(other.GetType().Name);
