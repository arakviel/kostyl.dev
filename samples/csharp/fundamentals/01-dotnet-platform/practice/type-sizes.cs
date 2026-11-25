// Практика 1: псевдонім C#, ім'я CTS і розмір у байтах для вбудованих типів.
Print("byte", typeof(byte), sizeof(byte));
Print("short", typeof(short), sizeof(short));
Print("int", typeof(int), sizeof(int));
Print("long", typeof(long), sizeof(long));
Print("float", typeof(float), sizeof(float));
Print("double", typeof(double), sizeof(double));
Print("decimal", typeof(decimal), sizeof(decimal));
Print("char", typeof(char), sizeof(char));
Print("bool", typeof(bool), sizeof(bool));

static void Print(string alias, Type type, int size) =>
    Console.WriteLine($"{alias,-8} {type.FullName,-15} {size,2} Б");
