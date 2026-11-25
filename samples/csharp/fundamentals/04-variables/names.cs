// Ідентифікатори: префікс @ дозволяє взяти ключове слово як ім'я, кирилиця теж допустима.
int @class = 11;
int вік = 19;
int _count = 2;

Console.WriteLine(@class + вік + _count);
Console.WriteLine(nameof(@class));
