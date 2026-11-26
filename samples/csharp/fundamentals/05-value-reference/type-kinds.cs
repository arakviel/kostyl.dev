using System.Text;

// Які типи значущі, а які посилальні: Type.IsValueType.
Show("int", typeof(int));
Show("double", typeof(double));
Show("decimal", typeof(decimal));
Show("bool", typeof(bool));
Show("char", typeof(char));
Show("DateTime", typeof(DateTime));
Show("(int, int)", typeof((int, int)));
Show("string", typeof(string));
Show("object", typeof(object));
Show("int[]", typeof(int[]));
Show("StringBuilder", typeof(StringBuilder));
Show("List<int>", typeof(List<int>));

static void Show(string name, Type type) =>
    Console.WriteLine($"{name,-14} {(type.IsValueType ? "значущий" : "посилальний")}");
