int[] prices = [100, 200, 300];

Discount(prices);
Console.WriteLine($"після Discount: {string.Join(", ", prices)}");

Replace(prices);
Console.WriteLine($"після Replace:  {string.Join(", ", prices)}");

// метод отримує копію посилання на той самий масив
static void Discount(int[] items)
{
    for (int i = 0; i < items.Length; i++)
    {
        items[i] = items[i] * 9 / 10;
    }
}

// присвоєння параметру змінює лише параметр, а не змінну викликача
static void Replace(int[] items)
{
    items = [1, 2, 3];
    items[0] = 999;
}
