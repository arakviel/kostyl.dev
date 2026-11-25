// Усі способи оголосити локальну змінну.
int count;                 // лише оголошення: значення ще немає
count = 3;                 // перше присвоєння
int total = 10;            // оголошення з ініціалізацією
int width = 4, height = 3; // кілька змінних одного типу
var title = "Звіт";        // тип виводить компілятор: string
const int MaxScore = 100;  // константа: значення відоме під час компіляції
int empty = default;       // значення за замовчуванням для int: 0

Console.WriteLine($"{count} {total} {width}x{height} {title} {MaxScore} {empty}");
