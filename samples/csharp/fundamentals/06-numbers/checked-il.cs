// IL: звичайне додавання — add, у checked — add.ovf; приведення — conv.i4 і conv.ovf.i4.
Console.WriteLine(Add(1, 2));
Console.WriteLine(AddChecked(1, 2));
Console.WriteLine(ToInt(5L));
Console.WriteLine(ToIntChecked(5L));

static int Add(int a, int b) => a + b;
static int AddChecked(int a, int b) => checked(a + b);
static int ToInt(long value) => (int)value;
static int ToIntChecked(long value) => checked((int)value);
