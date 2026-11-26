// Міні-завдання: анонімний тип книжки.
var book = new { Title = "Кобзар", Year = 1840 };
Console.WriteLine(book);

var reprint = book with { Year = 1860 };
Console.WriteLine(reprint);

var copy = new { Title = "Кобзар", Year = 1840 };
Console.WriteLine(book.Equals(copy));
Console.WriteLine(book == copy);
