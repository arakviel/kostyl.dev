// 1. з кінця до початку: видалення не зсуває ще не перевірені елементи
List<int> numbers = [3, -1, -2, 4, -5];
for (int i = numbers.Count - 1; i >= 0; i--)
{
    if (numbers[i] < 0)
        numbers.RemoveAt(i);
}
Console.WriteLine($"з кінця: {string.Join(", ", numbers)}");

// 2. while: індекс збільшується лише тоді, коли елемент лишився
numbers = [3, -1, -2, 4, -5];
int index = 0;
while (index < numbers.Count)
{
    if (numbers[index] < 0)
        numbers.RemoveAt(index);
    else
        index++;
}
Console.WriteLine($"while: {string.Join(", ", numbers)}");
